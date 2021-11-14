import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from layout.banner import BANNER
from layout.footer import FOOTER
from API import fetch_div_legislators
from Data import Legislators


# APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title="Gender Diversity in Legislation")


################# CALLBACKS AND GRAPHS ####################

# Gender by Party Visualization
@app.callback(
    Output(component_id="gender_plot", component_property="figure"),
    [Input(component_id="party_dropdown", component_property="value")]
)
def gender_by_party_graph(party):
    # print(party)
    data = Legislators.data.query('party == "%s"' % party)
    # print(data)
    genders = data["gender"].unique()
    for i in range(len(genders)):
        if not genders[i]:
            genders[i] = "Unspecified"
    new_data = {
        "Gender": genders,
        "Count": [data.query("gender == '%s'" % gender).count()["name_full"] for gender in genders]
    }
    new_data_frame = pd.DataFrame(data=new_data)
    print(new_data)
    fig = {
        "data": [
            {"x": new_data_frame["Gender"], "y": new_data_frame["Count"], 'type': 'bar'}
        ],
        "layout": {
            "title": "Gender Count for %s Party" % party
        }
    }
    return fig



def main(app):
  
    ############ DATA ################
    
    # Legislators Data
    Legislators.fetch_data()
    parties = Legislators.data["party"].unique()
    parties.sort()
  
    ############# LAYOUT ###############
    
    # Sidebar
    sidebar = [
        # Sidebar Placeholder Explanatory Text
        html.P(
            "A little bit of explanatory text goes here if we want it. A little bit of explanatory text goes here if we want it. A little bit of explanatory text goes here if we want it.",
            className="text-italic font-weight-light",
            style = {"padding-top" : 100}
        ),
        # Sean's Face
        html.Img(
            src="https://media-exp1.licdn.com/dms/image/C5603AQF_Bbc8OPJppA/profile-displayphoto-shrink_400_400/0/1577748302235?e=1642636800&v=beta&t=S9VLy1dZK_haPe9-IJY2EJ3VlDxPT2dggsmMFzRli64",
            className = "rounded-circle img-fluid",
            height= "auto",
            style = {"padding-top" : 45}
        ),
        html.P(
            '"...change starts with you and I."',
            style = {"font-style" : "italic",
                     "text-align" : "center",
                     "padding-top" : 50}
        )
    ]
    
    # Single Select Card
    single_select_card = dbc.Col(
        dbc.Card(
            className = "border-2 border-primary h-100",
            children = html.Div(
                className = "card-body",
                children = [
                    html.Div(
                        html.H5(
                            "PLACEHOLDER",
                            className = "card-title text-light"
                        ),
                        style = {"padding" : 5, "padding-left" : 10},
                        className = "bg-primary rounded-top"                                ),
                    dbc.Label(
                        "Some placeholder single-category card:",
                        className="card-text"
                    ),
                    dbc.Row(
                        html.Div(
                            [
                                dbc.RadioItems(
                                    id="radios",
                                    className="btn-group",
                                    label_checked_class_name= "active",
                                    input_class_name = "btn-check",
                                    label_class_name= "btn btn-outline-primary",
                                    options=[
                                        {"label" : "Google", "value" : "GOOG"},
                                        {"label" : "Apple", "value" : "AAPL"},
                                        {"label" : "Amazon", "value" : "AMZN"},
                                    ],
                                ),
                                html.Div(id="output")
                            ],
                            className = "radio-group"
                        ),
                        justify = "center",
                    )
                ]
            )
        ),
        width = "auto",
        align = "stretch"
    )
    
    # Multi-Select Card
    multi_select_card = dbc.Col(
        dbc.Card(
            className = "border-2 border-primary h-100",
            children = html.Div(
                className = "card-body",
                children = [
                    html.Div(
                        html.H5(
                            "PLACEHOLDER",
                            className = "card-title text-light"
                        ),
                        style = {"padding" : 5, "padding-left" : 10},
                        className = "bg-primary rounded-top" 
                    ),
                    dbc.Label(
                        "Some multi-selector category:",
                        className="card-text"
                    ),
                    dbc.Row(
                        html.Div(
                            [
                                dbc.Checklist(
                                    id = "switches-input",
                                    switch = True,
                                    value = [1],
                                    options = [
                                        {"label" : "Google", "value" : "GOOG"},
                                        {"label" : "Apple", "value" : "AAPL"},
                                        {"label" : "Amazon", "value" : "AMZN"}
                                    ]
                                ),
                                html.Div(id="output2")
                            ],
                            className = "multi-group"
                        ),
                        justify = "center",
                    )
                ]
            )
        ),
        width = "auto",
        align = "stretch"
    )
    
    # Gender By Party Dropdown Card
    dropdown_gender_by_party_card = dbc.Col(
        dbc.Card(
            className = "border-2 border-primary h-100",
            children = html.Div(
                className = "card-body",
                children = [
                    html.Div(
                        html.H5(
                            "Political Party",
                            className = "card-title text-light"
                        ),
                        style = {"padding" : 5, "padding-left" : 10},
                        className = "bg-primary rounded-top" 
                    ),
                    dbc.Label(
                        "Select Party to Display:",
                        className="card-text"
                    ),
                    dbc.Row(
                        dbc.Select(
                            id = "party_dropdown",
                            options = [
                                {"label": value, "value": value} for value in parties
                            ]
                        ),
                        justify = "center",
                    )
                ]
            )
        ),
        width = "auto",
        align = "stretch"
    )
              
    # Full Layout
    app_layout = dbc.Container(
        [
            # Banner
            BANNER,
            dbc.Row(
                style={"padding" : 50}
            ),
            # Body
            dbc.Row(
                className = "gx-12",
                children = [   
                    # Sidebar
                    dbc.Col(
                        sidebar,
                        align = "stretch",
                        width = 3
                    ),                    
                    # Content
                    dbc.Col(
                        children = [
                            # Visualization
                            dcc.Graph(id="gender_plot"),
                            # Cards
                            dbc.Row(
                                justify = "center",
                                className = "d-flex flex-fill",
                                children = [
                                    # single_select_card,
                                    # multi_select_card,
                                    # Card for Drop Down List
                                    dropdown_gender_by_party_card,
                                ],
                            ),
                            # Footer
                            dbc.Row(style = {"padding" : 40}),
                            FOOTER  
                        ],
                        width = 9
                    )
                ]
            ),
        ]
    )
    
    # Run App
    app.layout = app_layout
    app.run_server(debug=True)
    

if __name__ == "__main__":
    main(app)