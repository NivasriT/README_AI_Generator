"""
Preview Callbacks for AI README Generator
Handles live markdown preview updates
"""

from dash import Input, Output


def register_preview_callbacks(app):
    """
    Register preview-related callbacks with the Dash app
    """
    
    @app.callback(
        Output('readme-preview', 'children'),
        Input('readme-editor', 'value'),
        prevent_initial_call=False
    )
    def update_preview(editor_content):
        """
        Update live preview when editor content changes
        """
        if editor_content is None or editor_content == "":
            # Return sample markdown if empty
            sample_markdown = """# Project Name

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
            return sample_markdown
        
        return editor_content
