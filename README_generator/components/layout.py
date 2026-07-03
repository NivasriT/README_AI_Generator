"""
Layout Component for AI README Generator
Main layout that combines all components
"""

from dash import html, dcc
from .header import create_header
from .sidebar import create_sidebar
from .editor_panel import create_editor_panel
from .preview_panel import create_preview_panel


def create_layout():
    """
    Create the main application layout

    Returns:
        Complete layout as Dash HTML
    """
    return html.Div([
        # Toast Notifications Container
        html.Div(id="notification-container", style={
            "position": "fixed",
            "top": "24px",
            "right": "24px",
            "zIndex": "9999",
            "display": "flex",
            "flexDirection": "column",
            "gap": "12px"
        }),

        # Header
        create_header(),

        # Main Content Area
        html.Div([
            # Left Sidebar
            html.Div([
                create_sidebar()
            ], className="sidebar-wrapper"),

            # Main Content (Editor + Preview) with Spinner Loader
            dcc.Loading(
                id="loading-panels",
                type="circle",
                color="#2563EB",
                parent_style={"flex": "1", "display": "flex"},
                children=html.Div([
                    # Editor Panel
                    html.Div([
                        create_editor_panel()
                    ], className="editor-wrapper"),

                    # Preview Panel
                    html.Div([
                        create_preview_panel()
                    ], className="preview-wrapper")
                ], className="main-content")
            )
        ], className="content-wrapper")
    ], id="app-root", className="app-container")
