from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv('Covid19VacunasAgrupadas.csv')


app = Dash(__name__, title="Vacunados por Covid")

app.layout = html.Div([
    html.Div([
        html.H1('Vacunados por Covid'),
        html.Img(src='assets/vacuna.png')
    ], className='banner'), 
    html.Div([
        html.Div([
            html.P(
                'Selecciona la dosis',
                className='fix_label',
                style={'color': 'black', 'marginTop': '2px'},
            ),
            dcc.RadioItems(
                id='dosis-radioItems',
                labelStyle={'display': 'inline-block'},
                options=[
                    {'label': 'Primera dosis', 'value': 'primera-dosis_cantidad'},
                    {'label': 'Segunda dosis', 'value': 'segunda-dosis_cantidad'},
                ], value='primera_dosis_cantidad',
                style={'text-align': 'center', 'color': 'black'}, className='dcc_compon'
            ),
        ], className='create-container2 five columns', style={'margin-bottom': '20px'}),
    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='my_graph', figure={})
        ], className='create-container2 eight columns'),
        html.Div([
            dcc.Graph(id='pie_graph', figure={})
        ], className='create-container2 five columns')
    ], className='row flex-display'),
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=8050)
    