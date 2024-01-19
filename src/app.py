from dash import html, dcc
from dash import Dash, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import random
import pandas as pd
import pathlib
import openpyxl

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
def get_pandas_data(dfordenada: str) -> pd.DataFrame:

   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath('../src/assets').resolve()
   return pd.read_excel(DATA_PATH.joinpath(dfordenada))

dfthe = get_pandas_data("the.xlsx")


lindex = list(dfthe.index)

lcol = dfthe['structure'].unique()

loptions = [{'label': str(option), 'value': option} for option in lcol]

card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/the.jpg", top=True, bottom=False,
                    title='logo', alt='check image route'),
        dbc.CardBody(
            [
                html.H4('TRANSLATION WARM-UP', className="card-title"),
                html.H6('CHOOSE A STRUCTURE', className="class-subtitle"),
                dcc.Dropdown(loptions, value='all', id='mydrop'),
                html.Div(id='container-button-timestamp0'),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('SPANISH', id='btn-nclicks-1', n_clicks=0,
                           color="info", className="me-1"),
                html.Div(id='container-button-timestamp'),
                dbc.Button('ENGLISH', id='btn-nclicks-2', n_clicks=0,
                           color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2'),
            ],
            # className="d-flex flex-column justify-content-center align-items-center",  # Center the card body content
        )
    ],

    color="danger",
    # inverse = True,
    outline=True,
    style={"width": "100%", "max-width": "800px", "margin": "auto"}
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(card_main, width={'size': 12}),
    ], justify='around', align='center'),
    dcc.Store(id="didfthe-stored", data=[]),
    dcc.Store(id="diordenadatoday-stored", data=[]),
],
    style={"width": "18rem"},
    fluid=False)


@app.callback(
    [Output('container-button-timestamp0', 'children'),
     Output("didfthe-stored", 'data')],
    [Input('mydrop', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
    if 'all' in selected_options:
        msg = 'You have selected: All option'
        didfthe = dfthe.to_dict('records')
        return html.Div(msg), didfthe
    else:
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfthe.loc[dfthe['structure'] == selected_options]
        didfthe = dffiltrada.to_dict('records')
        return html.Div(msg), didfthe


@app.callback(
    [Output('container-button-timestamp', 'children'),
     Output('diordenadatoday-stored', 'data')],
    [Input('btn-nclicks-1', 'n_clicks')],
    [State("didfthe-stored", 'data')],
    prevent_initial_call=True
)
def displayClick(btn1, didfthe):
    msg = "pulsa boton para una frase"

    if "btn-nclicks-1" in callback_context.triggered_id:
        dfthe = pd.DataFrame(didfthe)
        lindex = list(dfthe.index)
        randomn = random.choice(lindex)
        row = dfthe.iloc[[randomn]]
        esp = row.loc[:, 'esp']
        msg = esp
        diordenadatoday = row.to_dict('records')
        return html.Div(msg), diordenadatoday


@app.callback(
    Output('container-button-timestamp2', 'children'),
    [Input('btn-nclicks-2', 'n_clicks')],
    [State('diordenadatoday-stored', 'data')],
    prevent_initial_call=True
)
def displayClick2(btn2, diordenadatoday):
    msg = "pulsa boton para obtener solución"
    if "btn-nclicks-2" in callback_context.triggered_id:
        row = pd.DataFrame(diordenadatoday)
        eng = row.loc[:, 'eng']
        msg = eng

    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True,port =871)
