import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

BANNER = dbc.Row(
    dbc.Navbar(
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    [
                        html.H2(
                            "Examining Politicians:", 
                            className="text-light"
                                )
                    ],
                    width = "auto"
                ),
                justify = "center"
            )
        ),
    color="primary",
    dark = True,
    fixed = "top"
    )
)