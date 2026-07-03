"""
Sidebar Component for AI README Generator
Left sidebar with upload, generate, and download controls
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_sidebar():
    """
    Create the left sidebar component
    
    Returns:
        Sidebar component as Dash HTML
    """
    return html.Div([
        # Logo and Title Section
        html.Div([
            html.Div([
                html.I(
                    className="bi bi-file-earmark-text sidebar-logo",
                    style={"fontSize": "32px"}
                ),
                html.H4("AI README Generator", className="sidebar-title mt-2 mb-1"),
                html.P(
                    "Generate beautiful README files using AI",
                    className="sidebar-subtitle text-muted small"
                )
            ], className="text-center mb-4")
        ]),
        
        # Divider
        html.Hr(className="sidebar-divider"),
        
        # Upload ZIP Card
        html.Div([
            html.Label("Upload Project ZIP", className="sidebar-label fw-bold mb-2"),
            dcc.Upload(
                id='upload-zip',
                children=html.Div([
                    html.Div([
                        html.I(className="bi bi-cloud-arrow-up", style={"fontSize": "32px"}),
                        html.P("Drag & Drop or Click to Upload", className="mt-2 mb-1"),
                        html.P("Supported: .ZIP files", className="text-muted small mb-1"),
                        html.P("Max size: 50MB", className="text-muted small")
                    ], className="text-center")
                ]),
                className="upload-zone",
                style={
                    'width': '100%',
                    'height': '150px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center'
                },
                multiple=False,
                accept='.zip'
            ),
            html.Div(id='upload-filename', className="upload-filename mt-2 small text-muted")
        ], className="sidebar-card mb-4"),
        
        # Divider
        html.Hr(className="sidebar-divider"),
        
        # Generate README Button
        html.Div([
            dbc.Button(
                [
                    html.I(className="bi bi-lightning-charge me-2"),
                    "Generate README"
                ],
                id='generate-btn',
                color="primary",
                size="lg",
                className="w-100 generate-btn",
                style={
                    "background": "linear-gradient(135deg, #3B82F6 0%, #6366F1 100%)",
                    "border": "none",
                    "fontWeight": "600",
                    "padding": "12px"
                }
            )
        ], className="sidebar-card mb-4"),
        
        # Divider
        html.Hr(className="sidebar-divider"),
        
        # Download README Button
        html.Div([
            dcc.Download(id="download-readme"),
            dbc.Button(
                [
                    html.I(className="bi bi-download me-2"),
                    "Download README"
                ],
                id='download-btn',
                color="success",
                size="lg",
                className="w-100 download-btn",
                disabled=True,
                style={
                    "fontWeight": "600",
                    "padding": "12px"
                }
            )
        ], className="sidebar-card mb-4"),
        
        # Divider
        html.Hr(className="sidebar-divider"),
        
        # Status Card
        html.Div([
            html.Label("Status", className="sidebar-label fw-bold mb-2"),
            html.Div(
                [
                    html.Span(className="status-dot me-2"),
                    html.Span("No Project Uploaded", id='status-text', className="status-text")
                ],
                id='status-indicator',
                className="status-indicator"
            )
        ], className="sidebar-card mb-4"),
        
        # Spacer
        html.Div(style={"flex": "1"}),
        
        # Footer
        html.Div([
            html.Hr(className="sidebar-divider mb-3"),
            html.P(
                    "v1.0.0 • Made with Dash + Groq",
                    className="footer-text text-muted small text-center mb-0"
                )      ])
    ], className="sidebar")
