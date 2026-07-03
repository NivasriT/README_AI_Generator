"""
Editor Panel Component for AI README Generator
Left panel with markdown editor and toolbar
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_editor_panel():
    """
    Create the markdown editor panel component
    
    Returns:
        Editor panel component as Dash HTML
    """
    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.I(className="bi bi-markdown", style={"fontSize": "20px"}),
                html.H5("Markdown Editor", className="ms-2 mb-0 fw-bold")
            ], className="d-flex align-items-center"),
            html.P(
                "Edit your generated README",
                className="text-muted small mb-0"
            )
        ], className="panel-header d-flex justify-content-between align-items-center mb-3"),
        
        # Toolbar
        html.Div([
            html.Div([
                html.Span("Words: ", className="text-muted small"),
                html.Span("0", id='word-count', className="fw-bold small")
            ], className="toolbar-item me-3"),
            html.Div([
                html.Span("Chars: ", className="text-muted small"),
                html.Span("0", id='char-count', className="fw-bold small")
            ], className="toolbar-item me-3"),
            html.Div([
                dcc.Clipboard(
                    target_id='readme-editor',
                    id='copy-btn',
                    title="Copy README content",
                    className="toolbar-btn me-2 btn btn-outline-light btn-sm",
                    style={
                        "display": "inline-flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "cursor": "pointer",
                        "padding": "6px 8px",
                        "minWidth": "32px",
                        "height": "31px"
                    }
                ),
                dbc.Button(
                    html.I(className="bi bi-trash"),
                    id='clear-btn',
                    color="light",
                    size="sm",
                    className="toolbar-btn me-2",
                    outline=True
                ),
                dbc.Button(
                    html.I(className="bi bi-fullscreen"),
                    id='fullscreen-btn',
                    color="light",
                    size="sm",
                    className="toolbar-btn",
                    outline=True
                )
            ], className="d-flex")
        ], className="toolbar d-flex align-items-center mb-3"),
        
        # Editor Textarea
        html.Div([
            dcc.Textarea(
                id='readme-editor',
                placeholder="# Your AI-generated README will appear here...",
                className="editor-textarea",
                style={
                    'width': '100%',
                    'height': '100%',
                    'minHeight': '400px',
                    'resize': 'none',
                    'border': 'none',
                    'outline': 'none',
                    'backgroundColor': 'transparent',
                    'fontFamily': "'JetBrains Mono', 'Fira Code', monospace",
                    'fontSize': '14px',
                    'lineHeight': '1.7'
                }
            )
        ], className="editor-container", style={
            'flex': '1',
            'overflow': 'auto'
        })
    ], className="editor-panel panel")
