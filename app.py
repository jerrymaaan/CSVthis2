import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src import handler, calculation
import json

# -----------------------------
# open config
# -----------------------------
CONFIG_PATH = 'src/config.json'

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# -----------------------------
# create dash app
# -----------------------------
app = dash.Dash(__name__, title="CSVthis2")
# automatically loads icon if assets/favicon.ico is in project folder

# -----------------------------
# layout for dash app
# -----------------------------
app.layout = html.Div([
    html.H1("CSVthis2", style={'textAlign': 'center'}),

    html.Div(
        [
            html.Button(
                "Einstellungen",
                id='open-config',
                disabled=True,  # add functionality to change config.json with GUI someday
                style={'display': 'inline-block'}
            ),
            dcc.Upload(
                id='upload-data',
                children=html.Button("Datei auswählen"),
                multiple=False,  # one data at a time
                style={'display': 'inline-block'}
            ),
            dcc.Store(id='stored-data'),
            html.Label(
                "Keine Datei gewählt",
                id='uploaded-filename'
            ),
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '10px'},
    ),

    html.Div(
        [
            html.Div(
                [
                    html.Label("Graph oben:"),
                    dcc.Dropdown(
                        id='dropdown-top',
                        multi=True,
                        clearable=False
                    )
                ],
                style={'width': '45%', 'display': 'inline-block', 'padding': '5px'}
            ),

            html.Div(
                [
                    html.Label("Graph unten:"),
                    dcc.Dropdown(
                        id='dropdown-bottom',
                        multi=True,
                        clearable=False
                    )
                ],
                style={'width': '45%', 'display': 'inline-block', 'padding': '5px'}
            ),
        ],
        style={'textAlign': 'center'}
    ),

    dcc.Graph(id='subplot-graph', style={'height': '120vh', 'width': '100%'}),

    html.Button("Graph herunterladen", id='btn-download-graph'),

    dcc.Download(id='download-graph'),
])


# -----------------------------
# callback: upload file
# -----------------------------
@app.callback(
    Output('stored-data', 'data'),
    Output('uploaded-filename', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    prevent_initial_call=True
)
def upload_file(contents, filename):
    if contents is None:
        return dash.no_update

    new_label = "Datei: " + filename

    # return in the order of the outputs:
    # stored-data, uploaded-filename
    return contents, new_label  # only saves base64-string (in contents)


# -----------------------------
# callback: update dropdown options based on uploaded file
# -----------------------------
@app.callback(
    Output('dropdown-top', 'options'),
    Output('dropdown-top', 'value'),
    Output('dropdown-bottom', 'options'),
    Output('dropdown-bottom', 'value'),
    Input('stored-data', 'data')
)
def update_dropdowns(stored_data):
    if not stored_data:
        return dash.no_update

    # stored data from dcc.Upload to dataframe
    df = handler.stored_data_to_df(config, stored_data)

    # add new columns if own calculation exists
    df = calculation.add_col(df)

    options = [{'label': col, 'value': col} for col in df.columns]

    value_top = [df.columns[0]] if len(df.columns) > 0 else []
    value_bottom = [df.columns[1]] if len(df.columns) > 1 else value_top

    # return in the order of the outputs:
    # dropdown-top options, dropdown-top value, dropdown-bottom options, ...
    return options, value_top, options, value_bottom


# -----------------------------
# callback: plot graphs into figure
# -----------------------------
@app.callback(
    Output('subplot-graph', 'figure'),
    Input('dropdown-top', 'value'),
    Input('dropdown-bottom', 'value'),
    Input('stored-data', 'data')
)
def update_graph(top_signals, bottom_signals, stored_data):
    if not stored_data:
        return dash.no_update

    # stored data from dcc.Upload to dataframe
    df = handler.stored_data_to_df(config, stored_data)

    # add new columns and values if own calculation exists
    df = calculation.do_calc(df)

    # main plot
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.05,
        # subplot_titles=('top graph', 'bottom graph')
    )

    # top subplot
    for column_name in top_signals:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[column_name], mode='lines', name=column_name),
            row=1, col=1
        )

    # bottom subplot
    for column_name in bottom_signals:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[column_name], mode='lines', name=column_name),
            row=2, col=1
        )

    # layout
    fig.update_layout(
        legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'),
    )

    return fig


# -----------------------------
# callback: download as html
# -----------------------------
@app.callback(
    Output('download-graph', 'data'),
    Input('btn-download-graph', 'n_clicks'),
    State('subplot-graph', 'figure'),
    State('uploaded-filename', 'children'),
    prevent_initial_call=True,
)
def download(n_clicks, figure, children):
    if children == "Keine Datei gewählt":
        return dash.no_update

    # figs pull in as dicts for some reason so turn back to figure
    figure = go.Figure(figure)

    # creates download filename with uploaded filename
    text, uploaded_file = children.split(' ')  # removes 'Datei: ' which is also in the label

    try:
        uploaded_filename, file_extension = uploaded_file.split('.')  # removes file extension if exits
    except ValueError:
        uploaded_filename = uploaded_file

    download_filename = f'{uploaded_filename}_CSVthis2.html'

    return dict(content=figure.to_html(), filename=download_filename)


# -----------------------------
# run dash app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
