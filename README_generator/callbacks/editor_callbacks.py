"""
Editor Callbacks for AI README Generator
Handles editor interactions, word/char counts, clipboard copy status, and README file downloading
"""

from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc


def register_editor_callbacks(app):
    """
    Register editor-related callbacks with the Dash app
    """

    # 1. Toggle download-btn disabled status based on editor content
    @app.callback(
        Output('download-btn', 'disabled'),
        Input('readme-editor', 'value')
    )
    def toggle_download_button(editor_content):
        """
        Disable download button if there is no Markdown text in the editor
        """
        if not editor_content or not editor_content.strip():
            return True
        return False

    # 2. Handle README.md file download and trigger toast notification
    @app.callback(
        [Output('download-readme', 'data'),
         Output('notification-container', 'children', allow_duplicate=True)],
        [Input('download-btn', 'n_clicks')],
        [State('readme-editor', 'value')],
        prevent_initial_call=True
    )
    def handle_download(n_clicks, readme_content):
        """
        Export editor content as README.md file using Dash's download functionality
        """
        if not n_clicks or not readme_content or not readme_content.strip():
            return None, None

        success_toast = dbc.Toast(
            "README.md file downloaded successfully!",
            header="Download Successful",
            icon="success",
            duration=3000
        )
        return dcc.send_string(readme_content, filename="README.md"), success_toast

    # 3. Toast success notification for Copy to Clipboard action
    @app.callback(
        Output('notification-container', 'children', allow_duplicate=True),
        Input('copy-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def show_copy_notification(n_clicks):
        """
        Show success toast when markdown is copied to clipboard
        """
        if n_clicks:
            return dbc.Toast(
                "Markdown content copied to clipboard!",
                header="Content Copied",
                icon="info",
                duration=2500
            )
        return None

    # 4. Word and Character count metrics updater
    @app.callback(
        [Output('word-count', 'children'),
         Output('char-count', 'children')],
        Input('readme-editor', 'value')
    )
    def update_metrics(editor_content):
        """
        Update word & character metrics on the editor toolbar
        """
        if not editor_content:
            return "0", "0"

        char_count = len(editor_content)
        word_count = len(editor_content.split())
        return str(word_count), str(char_count)

    # 5. Clear button — wipe the editor content
    @app.callback(
        Output('readme-editor', 'value', allow_duplicate=True),
        Input('clear-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_editor(n_clicks):
        """
        Clear all content from the markdown editor
        """
        if n_clicks:
            return ""
        return ""

    # 6. Theme toggle — switch between light and dark mode
    @app.callback(
        [Output('app-root', 'className'),
         Output('theme-toggle-icon', 'className')],
        Input('theme-toggle-icon', 'n_clicks'),
        State('app-root', 'className'),
        prevent_initial_call=True
    )
    def toggle_theme(n_clicks, current_class):
        """
        Toggle between light and dark mode
        """
        if n_clicks:
            is_dark = 'dark-mode' in (current_class or '')
            if is_dark:
                return 'app-container', 'bi bi-moon theme-indicator'
            else:
                return 'app-container dark-mode', 'bi bi-sun theme-indicator'
        return 'app-container', 'bi bi-moon theme-indicator'
