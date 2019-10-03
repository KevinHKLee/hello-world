import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import json
from textwrap import dedent as d
import numpy as np
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
pd.options.mode.chained_assignment = None

PLOTLY_LOGO = "/assets/april.png"

def createdashboard(companyname,dashboardname,functions):
	return [
	    dbc.CardHeader(companyname, style = {'color':'white','font-size':'1.3vw', 'font-weight':'bold', 'font-family':'arial'}),
	    dbc.CardImg(src="/assets/RGE.png", top=True),
	    dbc.CardBody(
	        [   
	        	html.A(dashboardname, href='https://google.com', target='_blank', style = {'color':'white','font-size':'1.5vw', 'font-weight':'bold', 'font-family':'arial'}),
	            html.P(functions, className="card-text"),
	            html.A('Edit', href='https://google.com',style = {'color':'white','font-size':'1vw', 'font-weight':'bold', 'font-family':'arial'}),
	        ]
	    ),
	]

def createcomponent(companyname,dashboardname,functions,nindex):
	return [
	    dbc.CardHeader(companyname, style = {'color':'white','font-size':'1.3vw', 'font-weight':'bold', 'font-family':'arial'}),
	    dbc.CardImg(src="/assets/RGE.png", top=True),
	    dbc.CardBody(
	        children = [   
	        	html.A(dashboardname, href='https://google.com', target='_blank', style = {'color':'white','font-size':'1.5vw', 'font-weight':'bold', 'font-family':'arial'}),
	            html.P(functions, className="card-text"),
	            html.A('Edit', href='https://google.com',style = {'color':'white','font-size':'1vw', 'font-weight':'bold', 'font-family':'arial'}),
	        ],
	        id='component_id_{}'.format(nindex)
	    ),
	]



page1 = html.Div(
    [
	    dbc.Row(
	        [
	        	dbc.Col(
	        		[
				    	dbc.CardDeck(
				    		[		            
			                dbc.Card(createdashboard('Apical','SDS CPO Receiving and Consumption','Heny Sulistiowati'), color="success", inverse=True),
			                dbc.Card(createdashboard('Apical','CPO Discharging Report','Heny Sulistiowati'), color="secondary", inverse=True),
			                dbc.Card(createdashboard('Apical','CPO Truck Deliveries','Sandi Huang'), color="info", inverse=True),
			                ]
			            )

	        		],
	        		className="mb-2 mt-2 ml-2 mr-2",
	        	)
	        ],
	        className="mb-0",
	    ),

	    dbc.Row(
	        [
	        	dbc.Col(
	        		[
				    	dbc.CardDeck(
				    		[		            
			                dbc.Card(createdashboard('Apical','REF Non-Consistent Consumption','Herny Tomas'), color="primary", inverse=True),
			                dbc.Card(createdashboard('Apical','CPO Receiving and Consumption Status','Herny Tomas'), color="warning", inverse=True),
			                dbc.Card(createdashboard('Apical','Daily Refineries Operation Report','Mohamad Rohman'), color="danger", inverse=True),
			                ]
			            )

	        		],
	        		className="mb-2 mt-2 ml-2 mr-2",
	        	)
	        ],
	        className="mb-0",
	    ),
    ]
)

page2 = html.Div(
    [
	    dbc.Row(
	        [
	        	html.Div(
	        		children = [
	        			html.Button('Add Row', id='button_row'),
	        			html.Button('Add Col', id='button_col'),
	        			html.Button('Delete Row', id='button_row_del'),
	        		],
	        		id='page_button',
	        	),
	        ],
	    ),

    	html.Div(
    		children = [
    			html.P('Testing')
    		],
    		id='page_create',
    	),

	    html.Div(id='state_row', style={'display': 'none'}),

    ]
)

page3 = html.Div(
    [
	    dbc.Row(
	        [
	        	dbc.Col(
	        		[
				    	dbc.CardDeck(
				    		[		            
			                dbc.Card(createdashboard('Apical','SDS CPO Receiving and Consumption','Heny Sulistiowati'), color="success", inverse=True),
			                dbc.Card(createdashboard('Apical','CPO Discharging Report','Heny Sulistiowati'), color="secondary", inverse=True),
			                dbc.Card(createdashboard('Apical','CPO Truck Deliveries','Sandi Huang'), color="info", inverse=True),
			                ]
			            )

	        		],
	        		className="mb-2 mt-2 ml-2 mr-2",
	        	)
	        ],
	        className="mb-0",
	    ),
    ]
)




navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(dbc.NavbarBrand("RGE Business Intelligence Platform",className="ml-2", style={'font-size': '1.4rem'})),
                # dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", width="140px"), style={'text-align': 'right'}),
            ],
            # align="center",   
            no_gutters=True,
            style = {'flex': '1', 'justify-content':'space-between'}
        ),

    ],
    # color="dark",
    color = '#2F5DE2',
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
                                dbc.Button("Dashboards", id='btn-1', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black', 'font-weight':'bold'}),
                                dbc.Button("Create New Dashboard", id='btn-2', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black', 'font-weight':'bold'}),
                                dbc.Button("Add Data Source", id='btn-3', n_clicks_timestamp=0, style={'text-align':'left', 'border': 0, 'color': 'black', 'font-weight':'bold'}),
                            ],
                            vertical=True,
                            style={'width':'100%'}
                        ),
                    ],
                    xl=2,
                    md=2,
                    xs=2,
                    className="pt-2",
                    style={'background-color': '#f0f0f0', 'min-height': 'calc(100vh - 58px)', 'padding': '0 0 15px 0'}
                ),
                dbc.Col(
                    [

                        html.Div(id='page_container'),

                    ],
                    xl=10,
                    md=10,
                    xs=10,
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
app.title = 'RGE BIP'
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server


# Sidebar Menu
@app.callback(Output('page_container', 'children'),
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


@app.callback(
    dash.dependencies.Output('page_create', 'children'),
    [dash.dependencies.Input('button_row', 'n_clicks')],
    [dash.dependencies.State('state_row', 'value')])
def update_output(n_clicks, value):
	if not n_clicks:
		n_clicks = 0
	else:
		pass

	return html.Div(

		    	[	dbc.Row([
						dcc.RadioItems(
						    options=[
						        {'label': 'Row '+str(n_clicks), 'value': 'Row'+str(n_clicks)}
						    ],
						    labelStyle={'display': 'inline-block'}
						),
						dbc.Col(createcomponent('Apical','SDS CPO Receiving and Consumption','Heny Sulistiowati',n_clicks), width=4),
						
						# 'The row button has been clicked {} times, and col button {} times'.format(
				  #       	n_clicks,
				  #       	value
				  #   	),
		    		]) for i in range(max(1,n_clicks+1))]


		)



	# return html.Div(

	# 	    	[	dbc.Row([
	# 	                dcc.Dropdown(id='dropdown_id_{}'.format(n_clicks),
	# 	                options=[{'label': v, 'value': v} for v in ['select1', 'select2', 'select3']]),
	# 	                html.P('   '),
	# 					'The row button has been clicked {} times, and col button {} times'.format(
	# 			        	n_clicks,
	# 			        	value
	# 			    	),
	# 	    		]) for i in range(1,max(1,n_clicks))]


	# 	)
# cards = dbc.Row([dbc.Col(first_card, width=4), dbc.Col(second_card, width=8)])


@app.callback(
    dash.dependencies.Output('state_row', 'value'),
    [dash.dependencies.Input('button_col', 'n_clicks')])
def update_state(n_clicks):
    return n_clicks







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





