import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px


app = dash.Dash()

@app.callback(
    Output(component_id="stock_plot", component_property="figure"),
    [Input(component_id="dropdown", component_property="value")]
)
def update_graph(dropdown_value):
    if not dropdown_value:
        dropdown_value = "GOOG"
    data = px.data.stocks()
    print(dropdown_value)
    fig = go.Figure([
        go.Scatter(
            x=data["date"], 
            y=data[dropdown_value], 
            line={"color": "firebrick", "width": 4}
        )
    ])
    fig.update_layout(
        title="Stock Prices over Time",
        xaxis_title="Dates",
        yaxis_title="Prices"
    )
    return fig


def main(app):
    app.layout = html.Div(
        id="parent",
        children=[
            html.H1(
                id="H1", 
                children="Styling using HTML components",
                style={'textAlign':'center', 'marginTop':40,'marginBottom':40}
            ),
            dcc.Dropdown(
                id="dropdown",
                options=[
                    {"label": "Google", "value": "GOOG"},
                    {"label": "Apple", "value": "AAPL"},
                    {"label": "Amazon", "value": "AMZN"}
                ],
                value="GOOG",
                style={"width": 200}
            ),
            dcc.Graph(id="stock_plot")
        ]
    )
    app.css.append_css({
        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
    })
    app.run_server(debug=True)


if __name__ == "__main__":
    main(app)