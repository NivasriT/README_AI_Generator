"""
Preview Panel Component for AI README Generator
Right panel with live markdown preview
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_preview_panel():
    """
    Create the live preview panel component
    
    Returns:
        Preview panel component as Dash HTML
    """
    # Sample markdown for preview
    sample_markdown = r"""# Project Name

A brief description of what this project does and who it's for.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

```bash
pip install project-name
```

## Usage

```python
import project_name

# Your code here
```

## Contributing

Contributions are welcome!

## License

MIT License
"""
    
    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.I(className="bi bi-eye", style={"fontSize": "20px"}),
                html.H5("Live Preview", className="ms-2 mb-0 fw-bold")
            ], className="d-flex align-items-center"),
            html.P(
                "Rendered Markdown",
                className="text-muted small mb-0"
            )
        ], className="panel-header d-flex justify-content-between align-items-center mb-3"),
        
        # Preview Content
        html.Div([
            dcc.Markdown(
                id='readme-preview',
                children=sample_markdown,
                className="preview-content"
            )
        ], className="preview-container", style={
            'flex': '1',
            'overflow': 'auto'
        })
    ], className="preview-panel panel")
