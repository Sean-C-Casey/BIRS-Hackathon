import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

BANNER = dbc.Navbar(
    dbc.Container(
        children = dbc.Row(
            justify = "between",
            children = [
                dbc.Col(
                    html.A(
                        html.Img(
                            src="assets/icon.png",
                            height = "50px",
                        ),
                        href="#"
                    )
                ),
                dbc.Col(
                    html.H2(
                        "Diversity in Politics", 
                        className="text-light"
                            ),
                    width = "auto"
                ),
            ],
        )
    ),
    color="primary",
    dark = True,
    fixed = "top"
)