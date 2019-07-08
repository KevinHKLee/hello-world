import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output, State


# navbar =     dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
#         <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
#           <a class="navbar-brand" href="#">Navbar</a>
#           <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
#             <span class="navbar-toggler-icon"></span>
#           </button>

#           <div class="collapse navbar-collapse" id="navbarColor01">
#             <ul class="navbar-nav mr-auto">
#               <li class="nav-item active">
#                 <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
#               </li>
#               <li class="nav-item">
#                 <a class="nav-link" href="https://www.google.com.my">Features</a>
#               </li>
#               <li class="nav-item">
#                 <a class="nav-link" href="#">Pricing</a>
#               </li>
#               <li class="nav-item">
#                 <a class="nav-link" href="#">About</a>
#               </li>
#             </ul>
#             <form class="form-inline my-2 my-lg-0">
#               <input class="form-control mr-sm-2" type="text" placeholder="Search">
#               <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
#             </form>
#           </div>
#         </nav>
#     ''')

PLOTLY_LOGO = "/assets/april.png"

search_bar = dbc.Row(
    [
        # dbc.Col(dbc.Input(type="search", placeholder="Search")),
        # dbc.Col(
        #     dbc.Button("Search", color="primary", className="ml-2"),
        #     width="auto",
        # ),
        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("COMO Web",className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="#",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    # color="dark",
    color = '#2F4F4F',
    dark=True,
    style = {'padding':'6px','font-size':'40'}
)


# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Link", href="#")),
#         dbc.DropdownMenu(
#             nav=True,
#             in_navbar=True,
#             label="Menu",
#             children=[
#                 dbc.DropdownMenuItem("Entry 1"),
#                 dbc.DropdownMenuItem("Entry 2"),
#                 dbc.DropdownMenuItem(divider=True),
#                 dbc.DropdownMenuItem("Entry 3"),
#             ],
#         ),
#     ],
#     brand="Demo",
#     brand_href="#",
#     sticky="top",
# )

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Views"),
                        html.P('Dashboard'),
                        html.P('Maintenance Order'),
                        html.P('Monitoring'),

                        # dbc.Button("View details", color="secondary"),
                    ],
                    xl=2,
                    md=4,
                    xs=6,
                    className="pt-2",
                    style={'background-color': '#f0f0f0', 'min-height': 'calc(100vh - 71px)', 'padding-bottom': '15px'}
                ),
                dbc.Col(
                    [
                        html.H4("Graph"),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                        ),
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

if __name__ == "__main__":
    app.run_server(debug=True)
