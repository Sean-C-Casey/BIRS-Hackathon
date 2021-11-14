import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

FOOTER = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            justify = "center"
        )
    ),
    className="navbar-expand",
    color= "primary",
    dark = True,
    fixed = "bottom"
)