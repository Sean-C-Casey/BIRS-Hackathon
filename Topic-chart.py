from ipywidgets.widgets.widget import PROTOCOL_VERSION_MAJOR
import requests
# from settings import API_KEY, API_BASE_URL, API_HOST, API_DIV_LEGISLATORS
# from settings import API_DIV_LEGISLATION, API_FED_LEGISLATION, API_FED_LEGISLATORS
import json
import pandas as pd
import dash
import numpy as np
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_csv("/home/saisree/Documents/Charts/JS/trial/temp.csv",index_col=0, parse_dates=True)
new_data = df[-df['topic'].isnull()]
new_data = new_data[-new_data['province_territory'].isnull()]



# # initialize app
app = dash.Dash(__name__)

def get_options(list_provinces):
    dict_list = []
    for province in list_provinces:
        dict_list.append({'label': province, 'value': province})
    return dict_list


app.layout = html.Div(children = [
    dcc.Dropdown(
                id='provinces',
                options=get_options(new_data['province_territory'].unique()),
                multi=False,
                value = 'BC',
                
                placeholder="Select a province",
                style={'backgroundColor': 'white',
                        'width':'50%', 'display':'inline-block'}
                ), 
    
    dcc.Graph(id='hist', config={'displayModeBar': False})
                                ]
                    )

# # Update the histogram

@app.callback(Output('hist', 'figure'),
                [Input('provinces', 'value')])

def update_histogram(selected_dropdown_value):
    df_plot = df[df['province_territory'] == selected_dropdown_value]
    labels=df_plot['topic'].value_counts().index
    values=list(df_plot['topic'].value_counts())
    
    figure = px.pie(df_plot,values=values,names=labels,hole=0.3,color_discrete_sequence=px.colors.sequential.RdBu)

    return figure
    


# # Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
