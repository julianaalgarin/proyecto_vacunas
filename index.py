from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

NAME_FIXES = {
    'C�rdoba': 'Córdoba',
    'Entre R�os': 'Entre Ríos',
    'Neuqu�n': 'Neuquén',
    'R�o Negro': 'Río Negro',
    'Tucum�n': 'Tucumán',
}

df = pd.read_csv('Covid19VacunasAgrupadas.csv')
df['jurisdiccion_nombre'] = df['jurisdiccion_nombre'].replace(NAME_FIXES)

DOSE_COLUMNS = [
    ('primera_dosis_cantidad', 'Primera dosis', '#3B82F6'),
    ('segunda_dosis_cantidad', 'Segunda dosis', '#8B5CF6'),
    ('dosis_unica_cantidad', 'Dosis única', '#2FBF9F'),
    ('dosis_adicional_cantidad', 'Dosis adicional', '#F59E0B'),
    ('dosis_refuerzo_cantidad', 'Refuerzo', '#EC4899'),
]
DOSE_LABELS = {col: label for col, label, _ in DOSE_COLUMNS}

df_agg = df.groupby('jurisdiccion_nombre', as_index=False)[[c for c, _, _ in DOSE_COLUMNS]].sum()

TEAL_SCALE = ['#CDEDE3', '#8FE3D0', '#2FBF9F', '#1B8073', '#0F4C43']
PIE_COLORS = ['#2FBF9F', '#3B82F6', '#8B5CF6', '#F59E0B', '#EC4899', '#14B8A6', '#6366F1', '#F97316', '#94A3B8']
TOP_N_PIE = 8


def fmt_number(n):
    return f'{int(n):,}'.replace(',', '.')


def style_fig(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, family='Inter, sans-serif', color='#1b2a38'), x=0.02, xanchor='left'),
        font=dict(family='Inter, sans-serif', color='#1b2a38'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=20, t=50, b=10),
        height=560,
        separators=',.',
        hoverlabel=dict(bgcolor='white', font_size=13, font_family='Inter, sans-serif'),
    )
    return fig


def make_bar_figure(col):
    label = DOSE_LABELS[col]
    d = df_agg[['jurisdiccion_nombre', col]].sort_values(col, ascending=True)
    fig = px.bar(
        d, x=col, y='jurisdiccion_nombre', orientation='h',
        color=col, color_continuous_scale=TEAL_SCALE,
        text=col,
    )
    fig.update_traces(
        texttemplate='%{text:,.0f}', textposition='outside', cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>%{x:,.0f} dosis<extra></extra>',
        marker_line_width=0,
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_title=None, yaxis_title=None, showlegend=False)
    fig.update_xaxes(showgrid=True, gridcolor='#eef1f3', zeroline=False)
    fig.update_yaxes(showgrid=False, automargin=True)
    return style_fig(fig, f'{label} por jurisdicción')


def make_pie_figure(col):
    label = DOSE_LABELS[col]
    d = df_agg[['jurisdiccion_nombre', col]].sort_values(col, ascending=False)
    top = d.head(TOP_N_PIE).copy()
    rest_sum = d[col].iloc[TOP_N_PIE:].sum()
    if rest_sum > 0:
        rest_row = pd.DataFrame([{'jurisdiccion_nombre': 'Otras jurisdicciones', col: rest_sum}])
        top = pd.concat([top, rest_row], ignore_index=True)

    fig = px.pie(
        top, names='jurisdiccion_nombre', values=col, hole=0.55,
        color_discrete_sequence=PIE_COLORS,
    )
    fig.update_traces(
        textinfo='percent', textposition='inside',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} dosis (%{percent})<extra></extra>',
        marker=dict(line=dict(color='#ffffff', width=2)),
    )
    fig.update_layout(
        legend=dict(orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.02, font=dict(size=11)),
        annotations=[dict(
            text=f'<b>{fmt_number(top[col].sum())}</b><br><span style="font-size:11px;color:#66788a">Total</span>',
            showarrow=False, font=dict(size=18, color='#1b2a38'),
        )],
    )
    return style_fig(fig, f'Distribución de {label.lower()}')


def kpi_card(col, label, color):
    total = int(df[col].sum())
    return html.Div(className='kpi-card', style={'--kpi-color': color}, children=[
        html.P(label, className='kpi-label'),
        html.P(fmt_number(total), className='kpi-value'),
    ])


app = Dash(__name__, title='Vacunados por Covid')

app.layout = html.Div(className='app-container', children=[
    html.Div(className='header', children=[
        html.Div(className='header-content', children=[
            html.Img(src='assets/vacuna.png', className='header-icon'),
            html.Div([
                html.H1('Vacunación COVID-19', className='header-title'),
                html.P('Seguimiento de dosis aplicadas por jurisdicción en Argentina', className='header-subtitle'),
            ]),
        ]),
    ]),

    html.Div(className='main-content', children=[
        html.Div(className='kpi-row', children=[
            kpi_card(col, label, color) for col, label, color in DOSE_COLUMNS
        ]),

        html.Div(className='card filter-card', children=[
            html.P('Selecciona el tipo de dosis', className='filter-label'),
            dcc.RadioItems(
                id='dosis-radioItems',
                options=[{'label': label, 'value': col} for col, label, _ in DOSE_COLUMNS],
                value='primera_dosis_cantidad',
                className='pill-radio',
                inputClassName='pill-radio-input',
                labelClassName='pill-radio-label',
            ),
        ]),

        html.Div(className='charts-row', children=[
            html.Div(className='card chart-card', children=[
                dcc.Graph(id='my_graph', config={'displayModeBar': False}),
            ]),
            html.Div(className='card chart-card', children=[
                dcc.Graph(id='pie_graph', config={'displayModeBar': False}),
            ]),
        ]),
    ]),

    html.Footer(className='footer', children=[
        html.P('Datos de vacunación COVID-19 por jurisdicción · Construido con Dash + Plotly', style={'margin': 0}),
    ]),
])


@app.callback(
    Output('my_graph', component_property='figure'),
    [Input('dosis-radioItems', component_property='value')],
)
def update_graph(value):
    return make_bar_figure(value)


@app.callback(
    Output('pie_graph', component_property='figure'),
    [Input('dosis-radioItems', component_property='value')],
)
def update_graph_pie(value):
    return make_pie_figure(value)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)
