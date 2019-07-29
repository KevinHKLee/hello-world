import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
pd.options.mode.chained_assignment = None

# declare static components
PLOTLY_LOGO = "/assets/april.png"

# load data here

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(dbc.NavbarBrand("COMO Web",className="ml-2", style={'font-size': '1.4rem'})),
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", width="140px"), style={'text-align': 'right'}),
            ],
            # align="center",   
            no_gutters=True,
            style = {'flex': '1', 'justify-content':'space-between'}
        ),

    ],
    # color="dark",
    color = '#2F4F4F',
    dark=True,
    style = {'padding':'7px'}
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Dashboard", id='btn-1', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Maintenance Order", id='btn-2', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Monitoring", id='btn-3', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
                            ],
                            vertical=True,
                            style={'width':'100%'}
                        ),
                    ],
                    xl=2,
                    md=4,
                    xs=6,
                    className="pt-2",
                    style={'background-color': '#f0f0f0', 'min-height': 'calc(100vh - 58px)', 'padding': '0 0 15px 0'}
                ),
                dbc.Col(
                    [

                        html.Div(id='container-button-timestamp', children='Enter a value and press submit'),

                    ],
                    xl=10,
                    md=8,
                    xs=6,
                    className="pt-2",
                ),
            ],
        )
    ],
    style={'max-width':'100%'},
)

page1 = html.Div(
    [
        html.H4("Dashboard"),
        # html.Div(
        #     style={'padding': 3}
        # ),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                           2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                        y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                           350, 430, 474, 526, 488, 537, 500, 439],
                        name='Loss Cook',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                ],
                layout=go.Layout(
                    title='Loss Cook',
                    showlegend=False,
                    legend=go.layout.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='my-graph'
        )  

    ]
)

page2 = html.Div(
    [
        html.H4("Maintenance Order"),
        dcc.Graph(
            figure={"data": [{"x": [1, 2, 3], "y": [9, 3, 1]},{"x": [1, 2, 3], "y": [5, -5, -12]}]}
        ),

    ]
)

page3 = html.Div(
    [
        html.H4("Monitoring"),

        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),

    ]
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([navbar, body])
app.title = 'COMO'
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server

@app.callback(Output('container-button-timestamp', 'children'),
              [Input('btn-1', 'n_clicks_timestamp'),
               Input('btn-2', 'n_clicks_timestamp'),
               Input('btn-3', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3):
        msg = page1
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3):
        msg = page2
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2):
        msg = page3
    else:
        msg = page1
    return msg

    # return html.Div([
    #     html.Div('btn1: {}'.format(btn1)),
    #     html.Div('btn2: {}'.format(btn2)),
    #     html.Div('btn3: {}'.format(btn3)),
    #     html.Div(msg)
    # ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'assets'),
                                     'favicon.ico')

@app.server.route('/assests/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assests')
    return send_from_directory(static_folder, path)

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0',port=8050)
