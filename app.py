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
from Data import Legislators, Legislation

# APP
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Everybody Everywhere",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = None

################# CALLBACKS AND GRAPHS ####################

# Gender by Party and Province Visualization
@app.callback(
    Output("gender_by_party_by_province", "figure"),
    [Input("province_dropdown", "value")],
)
def gender_by_province_and_party(selected_dropdown_value):
    df = Legislators.data
    new_data = df[-df["gender"].isnull()]
    df_active_mp = new_data[new_data["is_active"] == True]
    df_plot = df_active_mp[
        df_active_mp["province_territory"] == selected_dropdown_value
    ]
    figure = px.histogram(
        df_plot,
        x="party",
        color="gender",
        height=310,
        barmode="group",
        color_discrete_map={"M": "lightblue", "F": "lightcoral"},
        title=f"Distribution of Gender for active MP's in {selected_dropdown_value}",
        template="simple_white",
    )
    return figure


# # Gender by Party Visualization
# @app.callback(
#     Output(component_id="gender_plot", component_property="figure"),
#     [Input(component_id="province_dropdown", component_property="value")]
# )
# def gender_by_party_graph(party):
#     # print(party)
#     data = Legislators.data.query('party == "%s"' % party)
#     # print(data)
#     genders = data["gender"].unique()
#     for i in range(len(genders)):
#         if not genders[i]:
#             genders[i] = "Unspecified"
#     new_data = {
#         "Gender": genders,
#         "Count": [data.query("gender == '%s'" % gender).count()["name_full"] for gender in genders]
#     }
#     new_data_frame = pd.DataFrame(data=new_data)
#     print(new_data)
#     fig = {
#         "data": [
#             {"x": new_data_frame["Gender"], "y": new_data_frame["Count"], 'type': 'bar'}
#         ],
#         "layout": {
#             "title": "Gender Count for %s Party" % party
#         }
#     }
#     return fig

# Bill by Province Pie Chart
@app.callback(
    Output("province_bill_pie", "figure"), [Input("province_dropdown", "value")]
)
def province_bill_pie_chart(selected_dropdown_value):
    df = Legislation.data
    new_data = df[-df["topic"].isnull()]
    new_data = new_data[-new_data["province_territory"].isnull()]
    df_plot = df[df["province_territory"] == selected_dropdown_value]
    labels = df_plot["topic"].value_counts().index
    values = list(df_plot["topic"].value_counts())
    figure = px.pie(
        df_plot,
        values=values,
        names=labels,
        hole=0.3,
        height=440,
        template="simple_white",
        color_discrete_sequence=px.colors.sequential.RdBu,
        title=f"Topics of Passed Bills in {selected_dropdown_value}",
    )
    figure.update_xaxes(visible=False)
    figure.update_yaxes(visible=False)
    return figure


def configure(app):

    ############ DATA ################

    # Fetch Data
    Legislators.fetch_data()
    Legislation.fetch_data()

    # Get Parties to make Dropdowns
    parties = Legislators.data["party"].unique()
    parties.sort()
    provinces = Legislation.data["province_territory"].unique()
    provinces.sort()

    ############# LAYOUT ###############

    # Sidebar Explanation Text
    sidebar_text_1 = "This dashboard uses data from IOTO International’s Goverlytics API to illustrate the gender diversity among the active members of Parliament in the different provinces of Canada."
    sidebar_text_2 = "Furthermore, a visualization of the different bill topics that were passed in previous years is presented. This gives us insight on what sectors each province is focussing their efforts on."
    # Select Province Card
    dropdown_province_selection_card = dbc.Col(
        dbc.Card(
            className="border-2 border-primary",
            children=html.Div(
                className="card-body",
                children=[
                    html.Div(
                        html.H5("Province", className="card-title text-light"),
                        style={"padding": 5, "padding-left": 10},
                        className="bg-primary rounded-top",
                    ),
                    dbc.Label("Select Province to Display:", className="card-text"),
                    dbc.Row(
                        dbc.Select(
                            id="province_dropdown",
                            value="BC",
                            options=[
                                {"label": value, "value": value} for value in provinces
                            ],
                        ),
                        justify="center",
                    ),
                ],
            ),
        ),
        align="stretch",
    )

    # # Select Party Card
    # dropdown_party_selection_card = dbc.Col(
    #     dbc.Card(
    #         className="border-2 border-primary h-100",
    #         children=html.Div(
    #             className="card-body",
    #             children=[
    #                 html.Div(
    #                     html.H5("Political Party", className="card-title text-light"),
    #                     style={"padding": 5, "padding-left": 10},
    #                     className="bg-primary rounded-top",
    #                 ),
    #                 dbc.Label("Select Party to Display:", className="card-text"),
    #                 dbc.Row(
    #                     dbc.Select(
    #                         id="party_dropdown",
    #                         options=[
    #                             {"label": value, "value": value} for value in parties
    #                         ],
    #                     ),
    #                     justify="center",
    #                 ),
    #             ],
    #         ),
    #     ),
    #     width="auto",
    #     align="stretch",
    # )

    # # Single Select Card PLACEHOLDER
    # single_select_card = dbc.Col(
    #     dbc.Card(
    #         className="border-2 border-primary h-100",
    #         children=html.Div(
    #             className="card-body",
    #             children=[
    #                 html.Div(
    #                     html.H5("PLACEHOLDER", className="card-title text-light"),
    #                     style={"padding": 5, "padding-left": 10},
    #                     className="bg-primary rounded-top",
    #                 ),
    #                 dbc.Label(
    #                     "Some placeholder single-category card:", className="card-text"
    #                 ),
    #                 dbc.Row(
    #                     html.Div(
    #                         [
    #                             dbc.RadioItems(
    #                                 id="radios",
    #                                 className="btn-group",
    #                                 label_checked_class_name="active",
    #                                 input_class_name="btn-check",
    #                                 label_class_name="btn btn-outline-primary",
    #                                 options=[
    #                                     {"label": "Google", "value": "GOOG"},
    #                                     {"label": "Apple", "value": "AAPL"},
    #                                     {"label": "Amazon", "value": "AMZN"},
    #                                 ],
    #                             ),
    #                             html.Div(id="output"),
    #                         ],
    #                         className="radio-group",
    #                     ),
    #                     justify="center",
    #                 ),
    #             ],
    #         ),
    #     ),
    #     width="auto",
    #     align="stretch",
    # )

    # # Multi-Select Card PLACEHOLDER
    # multi_select_card = dbc.Col(
    #     dbc.Card(
    #         className="border-2 border-primary h-100",
    #         children=html.Div(
    #             className="card-body",
    #             children=[
    #                 html.Div(
    #                     html.H5("PLACEHOLDER", className="card-title text-light"),
    #                     style={"padding": 5, "padding-left": 10},
    #                     className="bg-primary rounded-top",
    #                 ),
    #                 dbc.Label("Some multi-selector category:", className="card-text"),
    #                 dbc.Row(
    #                     html.Div(
    #                         [
    #                             dbc.Checklist(
    #                                 id="switches-input",
    #                                 switch=True,
    #                                 value=[1],
    #                                 options=[
    #                                     {"label": "Google", "value": "GOOG"},
    #                                     {"label": "Apple", "value": "AAPL"},
    #                                     {"label": "Amazon", "value": "AMZN"},
    #                                 ],
    #                             ),
    #                             html.Div(id="output2"),
    #                         ],
    #                         className="multi-group",
    #                     ),
    #                     justify="center",
    #                 ),
    #             ],
    #         ),
    #     ),
    #     width="auto",
    #     align="stretch",
    # )

    # Full Layout
    app_layout = dbc.Container(
        [
            # Banner
            BANNER,
            dbc.Row(style={"padding": 50}),
            # Body
            dbc.Row(
                className="gx-12",
                children=[
                    # Sidebar
                    dbc.Col(
                        children=[
                            dbc.Row(
                                justify="center",
                                # className="d-flex flex-fill",
                                children=[
                                    dbc.Col(
                                        [
                                            html.P(
                                                sidebar_text_1,
                                                className="text-italic font-weight-light",
                                                style={
                                                    "padding-top": 0,
                                                    "padding-bottom": 0,
                                                    "font-style": "italic",
                                                },
                                            ),
                                            html.P(
                                                sidebar_text_2,
                                                className="text-italic font-weight-light",
                                                style={
                                                    "padding-top": 0,
                                                    "padding-bottom": 14,
                                                    "font-style": "italic",
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            dbc.Row(
                                dropdown_province_selection_card,
                                justify="center",
                            ),
                        ],
                        align="center",
                        width=4,
                    ),
                    # Content
                    dbc.Col(
                        children=[
                            # Gender Visualization
                            dcc.Graph(id="gender_by_party_by_province"),
                            # Pie Vis
                            dcc.Graph(id="province_bill_pie"),
                        ],
                        width=8,
                    ),
                    # Footer
                    dbc.Row(style={"padding": 40}),
                    FOOTER,
                ],
            ),
        ]
    )

    # Run App
    app.layout = app_layout
    return app
    # server = app.server
    # app.run_server(debug=True)


# Temp debugging

app = configure(app)
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
