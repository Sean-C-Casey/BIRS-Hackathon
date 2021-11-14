import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from API import fetch_div_legislators
from Data import Legislators


app = dash.Dash()

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
    Legislators.fetch_data()
    parties = Legislators.data["party"].unique()
    parties.sort()
    app.layout = html.Div(
        id="parent",
        children=[
            html.H1(
                id="H1", 
                children="Styling using HTML components",
                style={'textAlign':'center', 'marginTop':40,'marginBottom':40}
            ),
            dcc.Dropdown(
                id="party_dropdown",
                options=[
                    {"label": value, "value": value} for value in parties
                ],
                value="Green",
                style={"width": 500}
            ),
            dcc.Graph(id="gender_plot")

        ]
    )
    app.css.append_css({
        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
    })
    app.run_server(debug=True)


if __name__ == "__main__":
    main(app)