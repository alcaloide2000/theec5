from dash import html, dcc
from dash import Dash, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import random
import pandas as pd
import pathlib
import openpyxl


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,"https://use.fontawesome.com/releases/v5.15.4/css/all.css"])
server = app.server

# fubtion to get data
def get_pandas_data(dfordenada: str) -> pd.DataFrame:
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath('../src/assets').resolve()
   return pd.read_excel(DATA_PATH.joinpath(dfordenada),sheet_name=None)

# GET THE DATA FROM EXCEL
dithe = get_pandas_data("the.xlsx")


# data for the translation warm up card
dfthe = dithe['warm']
lindex = list(dfthe.index)
lcol = dfthe['structure'].unique()
loptions = [{'label': str(option), 'value': option} for option in lcol]
# card for the warm up
card_warm = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-running fa-3x"), ' ',
              'TRANSLATION WARM-UP',html.I(className="fas fa-running fa-3x")],
            className="class-subtitle"
        ),
                dbc.CardBody(
            [
                html.H4(' CHOOSE A STRUCTURE', className="card-title"),

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
    style={"width": "100%", "max-width": "1200px", "margin": "auto"}
)
# data for the translation warm up card
dfreport = dithe['reportedsp']
lindexrep = list(dfreport.index)
lcolrep = dfreport['story'].unique()
loptionsrep = [{'label': str(option), 'value': option} for option in lcolrep]
# card for the warm up
card_rep = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-comments fa-3x"), ' ',
              'REPORTED SPEECH',html.I(className="fas fa-comments fa-3x")],
            className="class-subtitle"
        ),
        dbc.CardBody(
            [

                html.H4('CHOOSE A STORY', className="class-subtitle"),
                dcc.Dropdown(loptionsrep, value='karl and Ana', id='mydroprep'),
                html.Div(id='container-button-timestamp0rep'),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('DIRECT', id='btn-nclicksrep-1', n_clicks=0,
                           color="info", className="me-1"),
                html.Div(id='container-button-timestamprep'),
                dbc.Button('REPORTED', id='btn-nclicksrep-2', n_clicks=0,
                           color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2rep'),
            ],
            # className="d-flex flex-column justify-content-center align-items-center",  # Center the card body content
        )
    ],
    color="danger",
    # inverse = True,
    outline=True,
    style={"width": "100%", "max-width": "1200px", "margin": "auto"}
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src="/assets/the.jpg", style={'width': '50%', 'max-width': '600px', 'margin': 'auto'}))
    ], justify='center', align='center', className="mb-4"),
    dbc.Row([
        dbc.Col(card_warm, width={'size': 6}),
        dbc.Col(card_rep, width={'size': 6})

    ], justify='around', align='center'),
    dcc.Store(id="didfthe-stored", data=[]),
    dcc.Store(id="diordenadatoday-stored", data=[]),
    dcc.Store(id="didfreport-stored", data=[]),
    dcc.Store(id="diordenadarep-stored", data=[]),
    dcc.Store(id="dirow", data=[])
],
    # style={"width": "22rem"},
    fluid=False
)

# callbacks for the warm up
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

# callbacks for the reported speech
@app.callback(
    [Output('container-button-timestamp0rep', 'children'),
     Output("didfreport-stored", 'data')],
    [Input('mydroprep', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
    # if 'all' in selected_options:
    #     msg = 'You have selected: All option'
    #     didfreport = dfreport.to_dict('records')
    #     return html.Div(msg), didfreport
    # else:
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfreport.loc[dfreport['story'] == selected_options]
        didfreport = dffiltrada.to_dict('records')
        return html.Div(msg), didfreport


@app.callback(
    [Output('container-button-timestamprep', 'children'),
     Output('diordenadarep-stored', 'data'),
     Output('dirow', 'data')],
    [Input('btn-nclicksrep-1', 'n_clicks')],
    [State("didfreport-stored", 'data'),
     State("diordenadarep-stored", 'data')],
    prevent_initial_call=True
)
def displayClick(btn1, didfreport,diordenadarep):
    msg = "pulsa boton para una frase"

    if "btn-nclicksrep-1" in callback_context.triggered_id:
        dfreport = pd.DataFrame(didfreport)
        diordenadarep = diordenadarep or {'last_index': -1}  # Initialize state if not present
        last_index = diordenadarep.get('last_index', -1)  # Get last selected index
        if last_index + 1 >= len(dfreport):
            # Reset index if we reach the end
            last_index = -1
        next_index = last_index + 1
        row = dfreport.iloc[[next_index]]
        direct = row.loc[:, 'direct']
        msg = direct
        diordenadarep = {'last_index': next_index}  # Update state with new index
        print(diordenadarep)
        last_index = diordenadarep['last_index']
        print(last_index)
        row = dfreport.iloc[[last_index]]
        dirow = row.to_dict('records')
        print(dirow)
        return html.Div(msg), diordenadarep, dirow


@app.callback(
    Output('container-button-timestamp2rep', 'children'),
    [Input('btn-nclicksrep-2', 'n_clicks')],
    [State('dirow', 'data')],
    prevent_initial_call=True
)
def displayClick2(btn2, dirow):
    msg = "pulsa boton para obtener solución"
    if "btn-nclicksrep-2" in callback_context.triggered_id:
        row = pd.DataFrame(dirow)
        reported = row.loc[:,'reported']
        msg = reported

    return html.Div(msg)


if __name__ == '__main__':
    app.run_server(debug=True,port =871)
