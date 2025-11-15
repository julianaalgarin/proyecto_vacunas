from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv('Covid19VacunasAgrupadas.csv')


app = Dash(__name__, title="Vacunados por Covid")

app.layout = html.Div([
    html.Div([
        html.H1('Vacunados por Covid', style={'textAlign': 'center', 'color': 'white'}),
        html.Img(src='assets/vacuna.png', style={'height': '60px', 'width': 'auto'})
    ], className='banner', style={
        'backgroundColor': '#2C3E50', 
        'padding': '20px', 
        'display': 'flex', 
        'alignItems': 'center', 
        'justifyContent': 'space-between'
    }), 
    
    html.Div([
        html.P(
            'Selecciona la dosis:',
            style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold', 'marginBottom': '10px'}
        ),
        dcc.RadioItems(
            id='dosis-radioItems',
            options=[
                {'label': ' Primera dosis', 'value': 'primera-dosis_cantidad'},
                {'label': ' Segunda dosis', 'value': 'segunda-dosis_cantidad'},
            ], 
            value='primera-dosis_cantidad',
            style={'textAlign': 'center', 'fontSize': '16px'},
            labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#ECF0F1'}),

    
    html.Div([
        html.Div([
            dcc.Graph(id='my_graph', figure={})
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='pie_graph', figure={})
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'padding': '20px'}),
    
], style={'fontFamily': 'Arial, sans-serif'})

@app.callback(
    Output('my_graph', component_property='figure'),
    [Input('dosis-radioItems', component_property='value')]
)
def update_graph(value):
    if value == 'primera-dosis_cantidad':
        fig = px.bar(
            data_frame=df,
            x='jurisdiccion_nombre',
            y='primera_dosis_cantidad'
        )
    else:
        fig = px.bar(
            data_frame=df,
            x='jurisdiccion_nombre',
            y='segunda_dosis_cantidad'
        )
    return fig   

@app.callback(
    Output('pie_graph', component_property='figure'),
    [Input('dosis-radioItems', component_property='value')]
)
def update_graph_pie(value):
    if value == 'primera-dosis_cantidad':
        fig2 = px.pie(
            data_frame=df,
            names='jurisdiccion_nombre',
            values='primera_dosis_cantidad'
        )
    else:
        fig2 = px.pie(
            data_frame=df,
            names='jurisdiccion_nombre',
            values='segunda_dosis_cantidad'
        )
    return fig2
       



if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=8050)
    