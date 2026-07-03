"""
AI README Generator - Main Dash Application
A web application that generates README.md files from uploaded project ZIP files using Google Gemini AI.
"""

import dash
from dash import Dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os
from components.layout import create_layout
from callbacks.upload_callbacks import register_upload_callbacks
from callbacks.generate_callbacks import register_generate_callbacks
from callbacks.preview_callbacks import register_preview_callbacks
from callbacks.editor_callbacks import register_editor_callbacks

# Load environment variables
load_dotenv()

# Initialize Dash app with Bootstrap theme and custom CSS
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'assets/styles.css'
    ],
    suppress_callback_exceptions=True,
    title="AI README Generator"
)
server = app.server

# Set the layout using the component-based layout
app.layout = create_layout()

# Register callbacks
register_upload_callbacks(app)
register_generate_callbacks(app)
register_preview_callbacks(app)
register_editor_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
