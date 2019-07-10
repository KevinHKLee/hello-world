import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

# declare static components
PLOTLY_LOGO = "/assets/april.png"

# # connect to data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# initialize list of lists 
data = [['tom', 10], ['nick', 15], ['juli', 14]] 
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Name', 'Age']) 

# intialise data of lists. 
data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]} 
# Create DataFrame 
df = pd.DataFrame(data) 

# initialise data of lists. 
data = {'Name':['Tom', 'Jack', 'nick', 'juli'], 'marks':[99, 98, 95, 90]} 
# Creates pandas DataFrame. 
df = pd.DataFrame(data, index =['rank1', 'rank2', 'rank3', 'rank4']) 

# List1  
Name = ['tom', 'krish', 'nick', 'juli']  
# List2  
Age = [25, 30, 26, 22]  
# get the list of tuples from two lists.  
# and merge them by using zip().  
list_of_tuples = list(zip(Name, Age))  
# Assign data to tuples.  
list_of_tuples   
# Converting lists of tuples into  
# pandas Dataframe.  
df = pd.DataFrame(list_of_tuples, columns = ['Name', 'Age'])  

search_bar = dbc.Row(
    [
        # dbc.Col(dbc.Input(type="search", placeholder="Search")),
        # dbc.Col(
        #     dbc.Button("Search", color="primary", className="ml-2"),
        #     width="auto",
        # ),
        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", width="140px")),
    ],
    no_gutters=True,
    className="ml-auto",
    # style={'position': 'absolute', 'right': '10px', 'top': '5px'},
    # align="center",
)

navbar = dbc.Navbar(
    [
        # html.A(
        #     # Use row and col to control vertical alignment of logo / brand
        #     dbc.Row(
        #         [
        #             # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
        #             dbc.Col(dbc.NavbarBrand("COMO Web",className="ml-2", style={'font-size': '1.4rem'})),
        #         ],
        #         align="center",
        #         no_gutters=True,
        #     ),
        #     href="#",
        # ),

        dbc.Row(
            [
                # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                dbc.Col(dbc.NavbarBrand("COMO Web",className="ml-2", style={'font-size': '1.4rem'})),
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", width="140px"), style={'text-align': 'right'}),
            ],
            # align="center",   
            no_gutters=True,
            style = {'flex': '1', 'justify-content':'space-between'}
        ),

        # dbc.NavbarToggler(id="navbar-toggler"),
        # dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
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
                        # html.H4("Views", style={'padding-bottom':'15px'}),
                        # html.P('Dashboard', style={'padding-bottom':'6px'}),
                        # html.P('Maintenance Order', style={'padding-bottom':'6px'}),
                        # html.P('Monitoring', style={'padding-bottom':'6px'}),

                        dbc.ButtonGroup(
                            [
                                # dbc.Button("Dashboard",style={'text-align':'left', 'border': 0, 'color': 'black', 'background-color':'transparent'}),
                                # dbc.Button("Maintenance Order",style={'text-align':'left', 'border': 0, 'color': 'black', 'background-color':'transparent'}),
                                # dbc.Button("Monitoring",style={'text-align':'left', 'border': 0, 'color': 'black', 'background-color':'transparent'}),
                                dbc.Button("Dashboard",style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Maintenance Order",style={'text-align':'left', 'border': 0, 'color': 'black'}),
                                dbc.Button("Monitoring",style={'text-align':'left', 'border': 0, 'color': 'black'}),
                            ],
                            vertical=True,
                            style={'width':'100%'}
                        ),

                        # dbc.Button("View details", color="secondary"),
                    ],
                    xl=2,
                    md=4,
                    xs=6,
                    className="pt-2",
                    style={'background-color': '#f0f0f0', 'min-height': 'calc(100vh - 58px)', 'padding': '0 0 15px 0'}
                ),
                dbc.Col(
                    [
                        html.H4("Report"),

                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]},{"x": [1, 2, 3], "y": [7, 5, 12]}]}
                        ),

                        # dash_table.DataTable(
                        #     id='table',
                        #     columns=[{"name": i, "id": i} for i in df.columns],
                        #     data=df.to_dict('records'),
                        #     style_cell_conditional=[
                        #         {'if': {'column_id': 'Name'},
                        #          'width': '50px'},
                        #         {'if': {'column_id': 'Age'},
                        #          'width': '50px'},
                        #     ]
                        # ),
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




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([navbar, body])
app.title = 'COMO'
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

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
