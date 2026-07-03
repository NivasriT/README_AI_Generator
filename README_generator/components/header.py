"""
Header Component for AI README Generator
Top navigation bar with logo, title, and action buttons
"""

from dash import html
import dash_bootstrap_components as dbc


def create_header():
    """
    Create the top header component
    
    Returns:
        Header component as Dash HTML
    """
    return dbc.NavbarSimple(
        children=[
            # Logo and Title
            html.Div([
                html.I(
                    className="bi bi-file-earmark-text header-logo me-2",
                    style={"fontSize": "24px"}
                ),
                html.Span(
                    "AI README Generator",
                    className="header-title fw-bold"
                ),
                dbc.Badge(
                    "MVP",
                    color="primary",
                    className="ms-2 header-badge"
                )
            ], className="d-flex align-items-center"),
            
            # Right side actions — theme toggle only
            html.Div([
                html.I(
                    id="theme-toggle-icon",
                    className="bi bi-moon theme-indicator",
                    style={"fontSize": "20px", "cursor": "pointer", "transition": "all 0.3s ease"}
                )
            ], className="d-flex align-items-center")
        ],
        brand="",
        brand_href="#",
        color="dark",
        dark=True,
        className="custom-navbar",
        style={
            "padding": "12px 24px",
            "minHeight": "60px"
        }
    )
