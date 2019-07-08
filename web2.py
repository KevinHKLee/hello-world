import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html

navbar =     dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
          <a class="navbar-brand" href="#">Navbar</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item active">
                <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="https://www.google.com.my">Features</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Pricing</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">About</a>
              </li>
            </ul>
            <form class="form-inline my-2 my-lg-0">
              <input class="form-control mr-sm-2" type="text" placeholder="Search">
              <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
            </form>
          </div>
        </nav>
    ''')


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
                        html.H2("Heading"),
                        html.P(
                            """\
Donec id elit non mi porta gravida at eget metus.
Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum
nibh, ut fermentum massa justo sit amet risus. Etiam porta sem
malesuada magna mollis euismod. Donec sed odio dui. Donec id elit non
mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus
commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit
amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed
odio dui."""
                        ),
                        dbc.Button("View details", color="secondary"),
                    ],
                    xl=2,
                    md=4,
                    xs=6,
                    className="pt-3",
                    style={'background-color': 'lightgreen', 'min-height': 'calc(100vh - 71px)', 'padding-bottom': '15px'}
                ),
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                        ),
                    ],
                    xl=10,
                    md=8,
                    xs=6
                ),
            ],
        )
    ],
    style={'max-width':'100%'},
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([navbar, body])

# app.layout = html.Div([
#     dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
#         <h1>Header</h1>
#     '''),
# ])


if __name__ == "__main__":
    app.run_server(debug=True)

