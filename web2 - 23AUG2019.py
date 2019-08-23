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
import loss_cook as losscook
import json
from textwrap import dedent as d
import sql_lib as sqllib
import numpy as np
import data_preprocessing as datapre

import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory

UPLOAD_DIRECTORY = "/uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)









# declare static components
PLOTLY_LOGO = "/assets/april.png"

# load loss cook data here
df = losscook.load_2019_data()
print(df.shape)


# load reliability data here
file_name = 'monthly_data_reliability_maint_raw.xlsx'
dfs = pd.read_excel(file_name, sheet_name=None)
dfs1 = dfs['Sheet1']

apr_mask = dfs1['Period'].map(lambda x: x.month) == 4
dfs1apr = dfs1[apr_mask]

# woodyard 12 & chip screen
dfWY12CS = dfs1[dfs1['Area']==dfs1['Area'].unique()[0]]






# Content Functions
def generate_table(textlist):
    return dbc.Table(
        # Header
        # [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # [html.Tr([html.Th('First'),html.Th('Second')])] +

        # Body
        [
            html.Tr([
                html.Td('Date'),
                html.Td(': '+str(textlist[0]))
            ]),
            html.Tr([
                html.Td('Short Fall (ADT)'),
                html.Td(': '+str(textlist[1]))
            ]),
            html.Tr([
                html.Td('Area'),
                html.Td(': '+str(textlist[4]))
            ]),
            html.Tr([
                html.Td('Equipment'),
                html.Td(': '+str(textlist[2]))
            ]),
            html.Tr([
                html.Td('Responsibility'),
                html.Td(': '+str(textlist[3]))
            ]),
            html.Tr([
                html.Td('Problem'),
                html.Td(': '+str(textlist[5]))
            ]),
        ], 
        borderless=True,
        size='sm',

        # [html.Tr([
        #     html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        # ]) for i in range(min(len(dataframe), max_rows))]
    )

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
                dbc.Col(dbc.NavbarBrand("Predictive Maintenance Digital Platform",className="ml-2", style={'font-size': '1.4rem'})),
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
                                dbc.Button("Reliability Maintenance Dashboard", id='btn-1', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Loss Cook Analysis", id='btn-2', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Oil Analysis", id='btn-3', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black'}),
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

                        html.Div(id='container-button-timestamp'),

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

page2 = html.Div(
    [
        html.H4("Loss Cook Analytics"),
        # html.Div(
        #     style={'padding': 3}
        # ),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=df['Date'],
                        y=df['Short Fall (Adt)']*-1,
                        customdata=df['Equipment']+','+df['Responsibility']+','+df['Area']+','+df['Problems'],
                        name='Loss Cook',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        ),
                        # hover = 
                    ),
                ],
                layout=go.Layout(
                    title='Loss Cook Trend',
                    showlegend=False,
                    legend=go.layout.Legend(
                        x=0,
                        y=1.0
                    ),
                    xaxis=dict(
                        title='Date',
                        titlefont=dict(
                            family='Courier New',
                            size=18,
                            color='black'
                        )
                    ),
                    yaxis=dict(
                        title='Short Fall (ADT)',
                        titlefont=dict(
                            family='Courier New',
                            size=18,
                            color='black'
                        )
                    ),
                    xaxis_range=['2019-01-01','2019-3-31'],
                    xaxis_rangeslider_visible=False,
                    margin=go.layout.Margin(l=80, r=0, t=40, b=40),
                    clickmode='event+select',
                )
            ),

            style={'height': 300},
            config = {'displayModeBar':False,
                        'scrollZoom': True,
                        'responsive': True,
            },
            animate = True,
            id='basic-interactions'
        ),


        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [

                                html.Div([
                                    # dcc.Markdown(d("""
                                    #     **Loss Cook Details**
                                    # """)),
                                    html.Div(id='losscooktable'),

                                ]),

                            ],
                            xl=6,
                            md=6,
                            xs=6,
                            className="pt-2",
                        ),

                        dbc.Col(
                            [

                                html.Div([
                                    # dcc.Markdown(d("""
                                    #     **Measurement Points**
                                    # """)),
                                    html.Div(id='losscookequipmentpoints'),
                                ]),

                            ],
                            xl=6,
                            md=6,
                            xs=6,
                            className="pt-2",
                        ),


                    ],
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [

                                html.Div([
                                    # dcc.Markdown(d("""
                                    #     **Loss Cook Details**
                                    # """)),
                                    # html.P('Results 1'),
                                    html.Div(id='results1'),

                                ]),

                            ],
                            xl=12,
                            md=12,
                            xs=12,
                            className="pt-2",
                        ),

                        # dbc.Col(
                        #     [

                        #         html.Div([
                        #             # dcc.Markdown(d("""
                        #             #     **Measurement Points**
                        #             # """)),
                        #             # html.P('Results 2'),
                        #             html.Div(id='results2'),
                        #         ]),

                        #     ],
                        #     xl=4,
                        #     md=4,
                        #     xs=4,
                        #     className="pt-2",
                        # ),

                        # dbc.Col(
                        #     [

                        #         html.Div([
                        #             # dcc.Markdown(d("""
                        #             #     **Measurement Points**
                        #             # """)),
                        #             # html.P('Results 3'),
                        #             html.Div(id='results3'),
                        #         ]),

                        #     ],
                        #     xl=4,
                        #     md=4,
                        #     xs=4,
                        #     className="pt-2",
                        # ),

                    ],
                )

            ],
            style={'max-width':'100%'},
        ),

        html.Div(id='intermediate-value', style={'display': 'none'}),

        html.Div(
            style={'padding': 30}
        ),


    ]
)



# Content Pages

page1 = html.Div(
    [
        html.H4("Reliability Maintenance Dashboard"),
        html.Div(
            style={'padding': 10}
        ),

        dbc.Row([

            dbc.Col([

                dcc.Graph(

                    figure=go.Figure(
                        data=[

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1['Less than 4 weeks'],
                                name='Less than 4 weeks',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='green',
                                )
                            ),

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1['5 - 11 weeks'],
                                name='5 - 11 weeks',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='yellow',
                                )
                            ),

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1['More than 12 weeks'],
                                name='More than 12 weeks',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='red',
                                )
                            ),

                        ],
                        layout=go.Layout(
                            title='Age of Finding [April 2019]',
                            showlegend=True,
                            barmode='stack',
                            yaxis=go.layout.YAxis(automargin=True,autorange="reversed"),
                            # xaxis=go.layout.XAxis(automargin=True),
                            margin={'t': 40,'b':40},
                        ),

                    ),


                    style={'height': 220},
                    config = {'displayModeBar':False,
                                # 'scrollZoom': True,
                                # 'responsive': True,
                    },
                    animate = True,
                    id='rmd2'

                ),

            ]),
        ]),

        dbc.Row([
            dbc.Col([

                dcc.Graph(

                    figure=go.Figure(
                        data=[

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1.Low,
                                name='Low',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='green',
                                )
                            ),

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1.Medium,
                                name='Medium',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='yellow',
                                )
                            ),

                            go.Bar(
                                y=dfs1.Area,
                                x=dfs1.High,
                                name='High',
                                orientation = 'h',
                                marker=go.bar.Marker(
                                    color='red',
                                )
                            ),

                        ],
                        layout=go.Layout(
                            title='Severity Grade [April 2019]',
                            showlegend=True,
                            barmode='stack',
                            yaxis=go.layout.YAxis(automargin=True, autorange="reversed"), 
                            margin={'t': 40,'b':40},
                        )
                    ),


                    style={'height': 220},
                    config = {'displayModeBar':False,
                                # 'scrollZoom': True,
                                # 'responsive': True,
                    },
                    animate = True,
                    id='rmd1'

                ),


            ]),

        ]),

        html.Div(id='rmdPart2'),



    ]
)




page3 = html.Div(
    [
        html.H3("RCM Oil Analysis Dashboard"),
        html.Div(
            style={'padding': 5}
        ),

        dbc.Row([
            dbc.ButtonGroup(
                [
                             
                    dbc.Button("Overview", id='OA-btn-1', n_clicks_timestamp=0, outline=True, color="primary", className="mr-1 ml-3"),
                    dbc.Button("New Analysis Request", id='OA-btn-2', n_clicks_timestamp=0, outline=True, color="primary", className="mr-1"),
                    dbc.Button("Outstanding Analysis", id='OA-btn-3', n_clicks_timestamp=0, outline=True, color="primary", className="mr-1"),
                    dbc.Button("Completed Reports", id='OA-btn-4', n_clicks_timestamp=0, outline=True, color="primary", className="mr-1"),

                ],
            ),
        ]),

        html.Div(
            style={'padding': 10}
        ),
        html.Div(id='oil-analysis-container'),
        html.Div(
            style={'padding': 50}
        ),

        # dbc.Row(dbc.Col(html.Div("A single column"))),
        # dbc.Row(
        #     [
        #         dbc.Col(html.Div("One of three columns")),
        #         dbc.Col(html.Div("One of three columns")),
        #         dbc.Col(html.Div("One of three columns")),
        #     ],
        #     no_gutters=True,
        # ),

        # dcc.Upload(
        #     id='upload-data',
        #     children=html.Div([
        #         'Drag and Drop or ',
        #         html.A('Select Files')
        #     ]),
        #     style={
        #         'width': '100%',
        #         'height': '60px',
        #         'lineHeight': '60px',
        #         'borderWidth': '1px',
        #         'borderStyle': 'dashed',
        #         'borderRadius': '5px',
        #         'textAlign': 'center',
        #         'margin': '10px'
        #     },
        #     # Allow multiple files to be uploaded
        #     multiple=True
        # ),
        # html.Div(id='output-data-upload'),

    ]
)

OA_page1 = html.Div(
    [
        # html.H4("Overview"),
        html.Div(
            style={'padding': 0}
        ),

        dbc.Row([

            dbc.Card(
                [
                    dbc.CardImg(src="/assets/april.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Oil Sample", className="card-title"),
                            html.P(
                                "Notifications",

                                className="card-text",
                            ),
                            dbc.Button("Search", color="primary"),
                        ]
                    ),
                ],
                style={"width": "15rem"},
                className = "mr-2 ml-3",
            ),

            dbc.Card(
                [
                    dbc.CardImg(src="/assets/april.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("MO02", className="card-title"),
                            html.P(
                                "Maintenance Order",

                                className="card-text",
                            ),
                            dbc.Button("Search", color="primary"),
                        ]
                    ),
                ],
                style={"width": "15rem"},
                className = "mr-2",
            ),

            dbc.Card(
                [
                    dbc.CardImg(src="/assets/april.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Completed Reports", className="card-title"),
                            html.P(
                                "Oil Analysis Reports",
                                # "make up the bulk of the card's content.",
                                className="card-text",
                            ),
                            dbc.Button("Search", color="primary"),
                        ]
                    ),
                ],
                style={"width": "15rem"},
                className = "mr-2",
            ),





        ])



    ]
)

OA_page2 = html.Div(
    [

        # html.H1("New Analysis Request"),
        html.H4("Upload new analysis request here:"),
        html.Div(
            style={'padding': 3}
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "50%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),

        html.Div(
            style={'padding': 30}
        ),

        html.H4("Successfully Uploaded Files:"),
        html.Ul(id="file-list"),

        # html.H4("Oil Analysis - New Analysis Request"),
        # dcc.Graph(
        #     figure={"data": [{"x": [1, 2, 3], "y": [9, 3, 1]},{"x": [1, 2, 3], "y": [5, -5, -12]}]}
        # ),

    ]
)

OA_page3 = html.Div(
    [
        html.H4("Oil Analysis - Outstanding Analysis"),
        html.Ul(id="file-list-2"),

    ]
)

OA_page4 = html.Div(
    [
        html.H4("Oil Analysis - Completed Reports"),
        html.Ul(id="file-list-3"),
    ]
)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([navbar, body])
app.title = 'PMDP'
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server










































@app.callback(Output('rmdPart2', 'children'),
              [Input('btn-1', 'n_clicks_timestamp'),
               Input('btn-2', 'n_clicks_timestamp'),
               Input('btn-3', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3):
        msg =   html.Div(
                    [ 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(

                                    figure=go.Figure(
                                        data=[

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.Low,
                                                # text=dfWY12CS.Low,
                                                textposition='auto',
                                                # text=dfWY12CS.Low.apply(str),
                                                name='Low',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='green',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.Medium,
                                                name='Medium',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='yellow',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.High,
                                                # text=dfWY12CS.High.apply(str),
                                                name='High',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='red',
                                                )
                                            ),

                                        ],
                                        layout=go.Layout(
                                            # title='I. WOODYARD 12 & CHIP SCREEN: Severity Trend',
                                            title=go.layout.Title(
                                                text="I. WOODYARD 12 & CHIP SCREEN: Severity Trend",
                                                # xref="paper",
                                                x=0.1
                                            ),
                                            showlegend=True,
                                            barmode='stack',
                                            yaxis=go.layout.YAxis(automargin=True), 
                                            margin={'t': 40},
                                        )
                                    ),


                                    style={'height': 260},
                                    config = {'displayModeBar':False,
                                                # 'scrollZoom': True,
                                                # 'responsive': True,
                                    },
                                    animate = True,
                                    id='rmdA11'+str(i)
                                ),
                            ]),

                            dbc.Col([
                                dcc.Graph(

                                    figure=go.Figure(
                                        data=[

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['Less than 4 weeks'],
                                                name='Less than 4 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='green',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['5 - 11 weeks'],
                                                name='5 - 11 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='yellow',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['More than 12 weeks'],
                                                name='More than 12 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='red',
                                                )
                                            ),

                                        ],
                                        layout=go.Layout(
                                            # title='I. WOODYARD 12 & CHIP SCREEN: Age of Finding Trend',
                                            title=go.layout.Title(
                                                text="I. WOODYARD 12 & CHIP SCREEN: Age of Finding Trend",
                                                # xref="paper",
                                                x=0
                                            ),
                                            showlegend=True,
                                            barmode='stack',
                                            yaxis=go.layout.YAxis(automargin=True),
                                            margin={'t': 40},
                                        ),

                                    ),


                                    style={'height': 260},
                                    config = {'displayModeBar':False,
                                                # 'scrollZoom': True,
                                                # 'responsive': True,
                                    },
                                    animate = True,
                                    id='rmdA12'+str(i)

                                ),

                            ]),                           
                            
                        ])

                        for i in range(1,3)
                    ]
                )

    else:
        msg =   html.Div(
                    [ 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(

                                    figure=go.Figure(
                                        data=[

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.Low,
                                                # text=dfWY12CS.Low,
                                                textposition='auto',
                                                # text=dfWY12CS.Low.apply(str),
                                                name='Low',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='green',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.Medium,
                                                name='Medium',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='yellow',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS.High,
                                                # text=dfWY12CS.High.apply(str),
                                                name='High',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='red',
                                                )
                                            ),

                                        ],
                                        layout=go.Layout(
                                            # title='I. WOODYARD 12 & CHIP SCREEN: Severity Trend',
                                            title=go.layout.Title(
                                                text="I. WOODYARD 12 & CHIP SCREEN: Severity Trend",
                                                # xref="paper",
                                                x=0.1
                                            ),
                                            showlegend=True,
                                            barmode='stack',
                                            yaxis=go.layout.YAxis(automargin=True), 
                                            margin={'t': 40},
                                        )
                                    ),


                                    style={'height': 260},
                                    config = {'displayModeBar':False,
                                                # 'scrollZoom': True,
                                                # 'responsive': True,
                                    },
                                    animate = True,
                                    id='rmdA11'+str(i)
                                ),
                            ]),

                            dbc.Col([
                                dcc.Graph(

                                    figure=go.Figure(
                                        data=[

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['Less than 4 weeks'],
                                                name='Less than 4 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='green',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['5 - 11 weeks'],
                                                name='5 - 11 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='yellow',
                                                )
                                            ),

                                            go.Bar(
                                                x=dfWY12CS.Period,
                                                y=dfWY12CS['More than 12 weeks'],
                                                name='More than 12 weeks',
                                                # orientation = 'h',
                                                marker=go.bar.Marker(
                                                    color='red',
                                                )
                                            ),

                                        ],
                                        layout=go.Layout(
                                            # title='I. WOODYARD 12 & CHIP SCREEN: Age of Finding Trend',
                                            title=go.layout.Title(
                                                text="I. WOODYARD 12 & CHIP SCREEN: Age of Finding Trend",
                                                # xref="paper",
                                                x=0
                                            ),
                                            showlegend=True,
                                            barmode='stack',
                                            yaxis=go.layout.YAxis(automargin=True),
                                            margin={'t': 40},
                                        ),

                                    ),


                                    style={'height': 260},
                                    config = {'displayModeBar':False,
                                                # 'scrollZoom': True,
                                                # 'responsive': True,
                                    },
                                    animate = True,
                                    id='rmdA12'+str(i)

                                ),

                            ]),                           
                            
                        ])

                        for i in range(1,3)
                    ]
                )




    return msg











# Reactive Button 1
@app.callback(Output('OA-btn-1', 'className'),
              [Input('OA-btn-1', 'n_clicks_timestamp'),
               Input('OA-btn-2', 'n_clicks_timestamp'),
               Input('OA-btn-3', 'n_clicks_timestamp'),
               Input('OA-btn-4', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3, btn4):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4):
        msg = "mr-1 ml-3 active"
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4):
        msg = "mr-1 ml-3"
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4):
        msg = "mr-1 ml-3"
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3):
        msg = "mr-1 ml-3"
    else:
        msg = "mr-1 ml-3 active"
    return msg

# Reactive Button 2
@app.callback(Output('OA-btn-2', 'className'),
              [Input('OA-btn-1', 'n_clicks_timestamp'),
               Input('OA-btn-2', 'n_clicks_timestamp'),
               Input('OA-btn-3', 'n_clicks_timestamp'),
               Input('OA-btn-4', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3, btn4):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4):
        msg = "mr-1"
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4):
        msg = "mr-1 active"
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4):
        msg = "mr-1"
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3):
        msg = "mr-1"
    else:
        msg = "mr-1"
    return msg

# Reactive Button 3
@app.callback(Output('OA-btn-3', 'className'),
              [Input('OA-btn-1', 'n_clicks_timestamp'),
               Input('OA-btn-2', 'n_clicks_timestamp'),
               Input('OA-btn-3', 'n_clicks_timestamp'),
               Input('OA-btn-4', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3, btn4):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4):
        msg = "mr-1"
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4):
        msg = "mr-1"
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4):
        msg = "mr-1 active"
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3):
        msg = "mr-1"
    else:
        msg = "mr-1"
    return msg

# Reactive Button 4
@app.callback(Output('OA-btn-4', 'className'),
              [Input('OA-btn-1', 'n_clicks_timestamp'),
               Input('OA-btn-2', 'n_clicks_timestamp'),
               Input('OA-btn-3', 'n_clicks_timestamp'),
               Input('OA-btn-4', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3, btn4):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4):
        msg = "mr-1"
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4):
        msg = "mr-1"
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4):
        msg = "mr-1"
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3):
        msg = "mr-1 active"
    else:
        msg = "mr-1"
    return msg

# Oil Analysis Dashboard
@app.callback(Output('oil-analysis-container', 'children'),
              [Input('OA-btn-1', 'n_clicks_timestamp'),
               Input('OA-btn-2', 'n_clicks_timestamp'),
               Input('OA-btn-3', 'n_clicks_timestamp'),
               Input('OA-btn-4', 'n_clicks_timestamp')])
def displayClick(btn1, btn2, btn3, btn4):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4):
        msg = OA_page1
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4):
        msg = OA_page2
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4):
        msg = OA_page3
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3):
        msg = OA_page4
    else:
        msg = OA_page1
    return msg





# Machine Analytics Cards
@app.callback(Output("card-content", "children"),
              [ Input("tabs", "active_tab"),
                Input('intermediate-value', 'children'),
                Input('basic-interactions', 'clickData')])
def tab_content(active_tab,datastore1,clickData):
    if active_tab == "tab-1":

        if not datastore1:
            print('Results 1: Empty loss cook dataframe')
            dff = pd.DataFrame()
            return
        else:
            dff = pd.read_json(datastore1, orient='split')
            if len(dff)>0:
                dataOverall, dataTime, dataFreq = sqllib.extract_signal(dff)

                print('Analytics Plotting Data:')
                print(len(dataOverall))
                print(len(dataTime))
                print(len(dataFreq))

                if len(dataOverall)>0 and len(dataTime)>0 and len(dataFreq)>0:

                    return html.Div([
                        # Plot vibration signals here using TREEELEMID
                        # dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True),
                        html.P("Overall Value Trend"),
                        dbc.Table.from_dataframe(dataOverall[['measid','datestr','readingtype','overallvalue']], striped=True, bordered=True, hover=True),

                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Scatter(
                                        y=dataFreq['data'].iloc[0],
                                        x=dataFreq['freq'].iloc[0],
                                        name='freq1plot',
                                        marker_color='rgba(152, 0, 0, .8)'

                                    ),
                                ],
                                layout=go.Layout(
                                    title='Spectrum',
                                    showlegend=False,
                                    legend=go.layout.Legend(
                                        x=0,
                                        y=1.0
                                    ),
                                    xaxis=dict(
                                        title='Frequency',
                                        titlefont=dict(
                                            family='Courier New',
                                            size=18,
                                            color='black'
                                        )
                                    ),
                                    yaxis=dict(
                                        title='Amplitude',
                                        titlefont=dict(
                                            family='Courier New',
                                            size=18,
                                            color='black'
                                        )
                                    ),
                                    margin=go.layout.Margin(l=80, r=0, t=40, b=40),
                                )
                            ),

                            style={'height': 300},
                            config = {'displayModeBar':False,
                                        'scrollZoom': True,
                                        'responsive': True,
                            },
                            animate = True,
                            id='freq1'
                        ),

                        html.Div(
                            style={'padding': 15}
                        ),

                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Scatter(
                                        y=dataTime['data'].iloc[0],
                                        x=dataTime['time'].iloc[0],
                                        name='time1plot',
                                        marker_color='rgba(152, 0, 0, .8)'

                                    ),
                                ],
                                layout=go.Layout(
                                    title='Time Series',
                                    showlegend=False,
                                    legend=go.layout.Legend(
                                        x=0,
                                        y=1.0
                                    ),
                                    xaxis=dict(
                                        title='Time (s)',
                                        titlefont=dict(
                                            family='Courier New',
                                            size=18,
                                            color='black'
                                        )
                                    ),
                                    yaxis=dict(
                                        title='Velocity (mm/s)',
                                        titlefont=dict(
                                            family='Courier New',
                                            size=18,
                                            color='black'
                                        )
                                    ),
                                    margin=go.layout.Margin(l=80, r=0, t=40, b=40),
                                )
                            ),

                            style={'height': 300},
                            config = {'displayModeBar':False,
                                        'scrollZoom': True,
                                        'responsive': True,
                            },
                            animate = True,
                            id='time1'
                        ),




                    ])


                else:                  
                    dff = pd.DataFrame()
                    return

            else:
                dff = pd.DataFrame()
                return


    elif active_tab == "tab-2":
        return html.Div([
            html.P("Pending Oil Analysis Data Connector"),
        ])
    elif active_tab == "tab-3":
        return html.Div([
            html.P("Pending Thermography Data Connector"),
        ])
    elif active_tab == "tab-4":
        return html.Div([
            html.P("Pending MCSA Data Connector"),
        ])
    return html.P("This shouldn't ever be displayed...")


# Sidebar Menu
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

# Monitoring Page
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

# Loss cook plot interactions
@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


# Loss cook details
@app.callback(
    Output('losscooktable', 'children'),
    [Input('basic-interactions', 'clickData')])
def selected_losscook(clickData):
    if not clickData:
        print('No Click Detected')
        txt1 = ''
        txt2 = ''
        txt3 = ''
        return html.Div([
            # html.P(txt1),
            # html.P(txt2),
            # html.P(txt3),
        ])
    else:
        # print(clickData['points'][0]['x'])
        # print(clickData['points'][0]['y'])
        txt1 = clickData['points'][0]['x']
        txt2 = clickData['points'][0]['y']
        txt3 = clickData['points'][0]['customdata']

        # extract Responsibility text from custom data
        if len(txt3.split(','))>1 and len(txt3.split(',')[0])>2 and len(txt3.split(',')[1])>2:
            txt4 = str(txt3.split(',')[1])
            txt5 = str(txt3.split(',')[2])
            txt6 = str(txt3.split(',')[3])
        else:
            txt4 = ''
            txt5 = ''
            txt6 = ''

        # extract Equipment text from custom data
        txt3 = txt3.split(',')[0]
        if len(txt3)>0:
            txt3 = str(txt3)
        else:
            txt3 = ''

        # compile list of text
        textlist = [txt1,txt2,txt3,txt4,txt5,txt6]

        # txt3a = txt3.split(',')[0]
        # rdf = sqllib.select_equipment(txt3a)
        # print(rdf)

        return html.Div([
            html.P('Loss Cook Details',
                    style={'color':'black', 'font-size':20},
                ),
            # html.P('Date: '+str(txt1)),
            # html.P('Short Fall (ADT):'+str(txt2)),
            # html.P(txt3),
            # html.P(txt4),

            generate_table(textlist),
        ])


# Loss cook plot selection dataframe 
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('basic-interactions', 'clickData')])
def storing_losscook_table(clickData):
    if not clickData:
        # print('No Click Detected')
        return pd.DataFrame().to_json(date_format='iso', orient='split')
    else:
        # print(clickData['points'][0]['x'])
        # print(clickData['points'][0]['y'])
        txt1 = clickData['points'][0]['x']
        txt2 = clickData['points'][0]['y']
        txt3 = clickData['points'][0]['customdata']

        txt3a = txt3.split(',')[0]

        txt3a = txt3a.replace(' ','').split(';')
        txt3b = [x for x in txt3a if len(x)>0]
        if len(txt3b)>0:
            selequip = txt3b[0]
        else:
            selequip = "none"

        rdf = sqllib.select_equipment(selequip)

        if len(rdf)>0:
            rdf1 = rdf[['SLOTNUMBER','NAME','DESCRIPTION','UNIT','TREEELEMID']]
            rdf1.rename(columns={'SLOTNUMBER': 'SLOT'}, inplace=True)
            return rdf1.to_json(date_format='iso', orient='split')
        else:
            return pd.DataFrame().to_json(date_format='iso', orient='split')


# Consolidated Measurements
@app.callback(
    Output('losscookequipmentpoints', 'children'),
    [Input('basic-interactions', 'clickData')])
def show_measurement_points(clickData):
    if not clickData:
        print('No Click Detected')
        return html.Div([
        ])
    else:
        # print(clickData['points'][0]['x'])
        # print(clickData['points'][0]['y'])
        txt1 = clickData['points'][0]['x']
        txt2 = clickData['points'][0]['y']
        txt3 = clickData['points'][0]['customdata']

        print('\n\n')
        print(txt3)
        txt3a = txt3.split(',')[0]
        print(txt3a)
        txt3a = txt3a.replace(' ','').split(';')
        txt3b = [x for x in txt3a if len(x)>0]
        print(txt3b)
        
        if len(txt3b)>0:
            selequip = txt3b[0]
        else:
            selequip = "none"


        # add tabs to select equipment




        print('\n\n')

        rdf = sqllib.select_equipment(selequip)

        if len(rdf)>0:

            rdf1 = rdf[['SLOTNUMBER','NAME','DESCRIPTION','UNIT']]
            rdf1.rename(columns={'SLOTNUMBER': 'SLOT'}, inplace=True)

            # AI Prediction Results
            rdf1['SOURCE'] = 'SKF Vibration'
            # rdf1.iat[2,4]='ANOMALY'

            rdf1['id'] = rdf1['SLOT']
            rdf1.set_index('id', inplace=True, drop=False)
            # print(rdf1)

            return html.Div([
                # dbc.Card([

                    dbc.Tabs(
                        [
                            dbc.Tab(label="EQ 1", tab_id="tabequip-1"),
                            dbc.Tab(label="EQ 2", tab_id="tabequip-2"),
                            # use list comprehension here to auto generate tabs
                        ]
                    ),



                    html.P('Consolidated Measurements',
                            style={'color':'black', 'font-size':20},
                        ),
                    # html.P(txt1),
                    # html.P(txt2),
                    # html.P(txt3),
                    # dbc.Table.from_dataframe(rdf1, striped=True, bordered=True, hover=True),

                    dash_table.DataTable(
                        id='table_points',
                        columns=[{"name": i, "id": i} for i in rdf1.columns
                                    if i !='id'
                        ],
                        data=rdf1.to_dict('records'),

                        # filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        row_selectable="multi",
                        row_deletable=False,
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        page_size= 5,

                        
                        style_cell={'textAlign': 'left','border': '1px solid black'},
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Date', 'Region']
                        ],
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#EBF5FB'
                            },
                            {
                                'if': {
                                    'column_id': 'AI PREDICTION',
                                    'filter_query': '{AI PREDICTION} eq "ANOMALY"'
                                },
                                'backgroundColor': '#CB4335',
                                'color': 'white',
                            },
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }

                    ),

                    html.Div(id='datatable-interactivity-container'),

                # ])
            ])

        else:
            return html.Div([
                html.P('No Measurement Points Found',
                        style={'color':'black', 'font-size':20},
                    ),
            ])

# Consolidated Measurements Output
@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('table_points', 'derived_virtual_row_ids'),
     Input('table_points', 'selected_row_ids'),
     Input('table_points', 'active_cell'),
     Input('intermediate-value', 'children'),
     Input('basic-interactions', 'clickData')])
def update_graphs(row_ids, selected_row_ids, active_cell,datastore1,clickData):
    
    if not datastore1:
        print('empty dataframe')
        dff = pd.DataFrame()
    else:
        dff = pd.read_json(datastore1, orient='split')

    if selected_row_ids is None:
        selected_row_ids = []

    # print(row_ids)
    # print(selected_row_ids)
    # print(active_cell)

    if len(selected_row_ids)>0 and len(dff)>0:
        selected1 = [int(x)-1 for x in selected_row_ids]
        # print(selected1)
        selected2 = [str(x) for x in selected1]
        # print(dff.loc[selected1])


    if not clickData:
        print('No Click Detected')
    else:
        # print(clickData['points'][0]['x'])
        # print(clickData['points'][0]['y'])
        # print(clickData['points'][0]['customdata'])
        txt1 = clickData['points'][0]['x']
        txt2 = clickData['points'][0]['y']
        txt3 = clickData['points'][0]['customdata']


    return


# Machine Analytics
@app.callback(Output('results1', 'children'),
    [Input('intermediate-value', 'children'),
     Input('basic-interactions', 'clickData')])
def update_results1(datastore1,clickData):
    # continuous updating status is due to these inputs unable to be fully loaded

    if not clickData:
        print('Results 1: No Click Detected')
        return 
        # return html.Div([
        #     # html.P(txt1),
        # ])
    else:

        if not datastore1:
            print('Results 1: Empty loss cook dataframe')
            dff = pd.DataFrame()
            return
        else:
            dff = pd.read_json(datastore1, orient='split')

            if not clickData:
                print('Results 1: No Click Detected')

            else:
                print('Machine Analytics:')
                print(clickData['points'][0]['x'])
                print(clickData['points'][0]['y'])
                print(clickData['points'][0]['customdata'])
                txt1 = clickData['points'][0]['x']
                txt2 = clickData['points'][0]['y']
                txt3 = clickData['points'][0]['customdata']

            return html.Div([
                    html.P('Machine Analytics',
                            style={'color':'black', 'font-size':20},
                        ),
                    # html.P(selected_row_ids),
                    dbc.Card([
                        dbc.CardHeader(
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="Vibration Analysis", tab_id="tab-1"),
                                    dbc.Tab(label="Oil Analysis", tab_id="tab-2"),
                                    dbc.Tab(label="Thermography", tab_id="tab-3"),
                                    dbc.Tab(label="MCSA", tab_id="tab-4"),
                                ],
                                id="tabs",
                                active_tab="tab-1",
                                card = True,
                            ),
                        ),
                        dbc.CardBody(html.Div(id="card-content")),
                    ]),
                    
            ])


# # Machine Analytics
# @app.callback(Output('results1', 'children'),
#     [Input('table_points', 'derived_virtual_row_ids'),
#      Input('table_points', 'selected_row_ids'),
#      Input('table_points', 'active_cell'),
#      Input('intermediate-value', 'children'),
#      Input('basic-interactions', 'clickData')])
# def update_results1(row_ids, selected_row_ids, active_cell,datastore1,clickData):
#     # continuous updating status is due to these inputs unable to be fully loaded

#     if not clickData:
#         print('Results 1: No Click Detected')
#         return 
#         # return html.Div([
#         #     # html.P(txt1),
#         # ])
#     else:

#         if not datastore1:
#             print('Results 1: Empty loss cook dataframe')
#             dff = pd.DataFrame()
#             return
#         else:
#             dff = pd.read_json(datastore1, orient='split')

#             if selected_row_ids is None:
#                 selected_row_ids = []

#             print(row_ids)
#             print(selected_row_ids)
#             print(active_cell)

#             if len(selected_row_ids)>0 and len(dff)>0:
#                 selected1 = [int(x)-1 for x in selected_row_ids]
#                 print(selected1)
#                 print(dff.loc[selected1])
#                 # selected2 = [str(x) for x in selected1]

#             if not clickData:
#                 print('Results 1: No Click Detected')
#             else:
#                 print('Machine Analytics:')
#                 print(clickData['points'][0]['x'])
#                 print(clickData['points'][0]['y'])
#                 print(clickData['points'][0]['customdata'])
#                 txt1 = clickData['points'][0]['x']
#                 txt2 = clickData['points'][0]['y']
#                 txt3 = clickData['points'][0]['customdata']

#             return html.Div([
#                     html.P('Machine Analytics',
#                             style={'color':'black', 'font-size':20},
#                         ),
#                     # html.P(selected_row_ids),
#                     dbc.Card([
#                         dbc.CardHeader(
#                             dbc.Tabs(
#                                 [
#                                     dbc.Tab(label="Vibration Analysis", tab_id="tab-1"),
#                                     dbc.Tab(label="Oil Analysis", tab_id="tab-2"),
#                                     dbc.Tab(label="Thermography", tab_id="tab-3"),
#                                     dbc.Tab(label="MCSA", tab_id="tab-4"),
#                                 ],
#                                 id="tabs",
#                                 active_tab="tab-1",
#                                 card = True,
#                             ),
#                         ),
#                         dbc.CardBody(html.Div(id="card-content")),
#                     ]),
                    
#             ])

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

# @app.callback(
#     Output("file-list-2", "children"),
#     [Input("upload-data", "filename"), Input("upload-data", "contents")],
# )
# def update_output(uploaded_filenames, uploaded_file_contents):
#     """Save uploaded files and regenerate the file list."""

#     if uploaded_filenames is not None and uploaded_file_contents is not None:
#         for name, data in zip(uploaded_filenames, uploaded_file_contents):
#             save_file(name, data)

#     files = uploaded_files()
#     if len(files) == 0:
#         return [html.Li("No files yet!")]
#     else:
#         return [html.Li(file_download_link(filename)) for filename in files]

# @app.callback(
#     Output("file-list-3", "children"),
#     [Input("upload-data", "filename"), Input("upload-data", "contents")],
# )
# def update_output(uploaded_filenames, uploaded_file_contents):
#     """Save uploaded files and regenerate the file list."""

#     if uploaded_filenames is not None and uploaded_file_contents is not None:
#         for name, data in zip(uploaded_filenames, uploaded_file_contents):
#             save_file(name, data)

#     files = uploaded_files()
#     if len(files) == 0:
#         return [html.Li("No files yet!")]
#     else:
#         return [html.Li(file_download_link(filename)) for filename in files]





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