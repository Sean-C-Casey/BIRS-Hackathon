import requests
from settings import API_KEY, API_BASE_URL, API_HOST, API_DIV_LEGISLATORS
from settings import API_DIV_LEGISLATION, API_FED_LEGISLATION, API_FED_LEGISLATORS
import json
import pandas as pd
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv("/Users/14187/Documents/MDS/RANDOM/HACKATHON/TEST/temp.csv", index_col=0, encoding = "ISO-8859-1")
new_data = df[-df['gender'].isnull()]
df_active_mp = new_data[new_data['is_active'] == True]



app = dash.Dash(__name__)

def get_options(list_provinces):
    dict_list = []
    for i in list_provinces:
        dict_list.append({'label': i, 'value': i})
    print(dict_list)
    return dict_list

app.layout = html.Div(children = [
    dcc.Dropdown(
                id='province',
                options=get_options(df_active_mp['province_territory'].unique()),
                multi=False,
                value = 'BC',
                
                placeholder="Select a province",
                style={'backgroundColor': 'white',
                        'width':'50%', 'display':'inline-block'}
                ), 
    
    dcc.Graph(id='graph', config={'displayModeBar': False})
                                ]
                    )
# Update the histogram

@app.callback(Output('graph', 'figure'),
                [Input('province', 'value')])

def update_histogram(selected_dropdown_value):
    #print(selected_dropdown_value)
    df_plot = df_active_mp[df_active_mp['province_territory'] == selected_dropdown_value]
    figure = px.histogram(df_plot, x='party', color = 'gender', barmode='group',
                                
                                title = f"Distribution of gender for active MP's in {selected_dropdown_value}",
                                template = "simple_white")

    return figure
    


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

