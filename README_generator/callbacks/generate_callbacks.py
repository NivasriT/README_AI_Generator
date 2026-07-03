"""
Generate Callbacks for AI README Generator
Handles README generation using Gemini AI
"""

from dash import Input, Output, State, html, ctx
import dash_bootstrap_components as dbc
from services.groq_service import GeminiService
import callbacks.upload_callbacks as upload_callbacks

# Global Gemini service instance
gemini_service = GeminiService()


def register_generate_callbacks(app):
    """
    Register generation-related callbacks with the Dash app
    """
    
    @app.callback(
        [Output('readme-editor', 'value'),
         Output('status-text', 'children', allow_duplicate=True),
         Output('status-indicator', 'className', allow_duplicate=True),
         Output('notification-container', 'children', allow_duplicate=True)],
        [Input('generate-btn', 'n_clicks')],
        [State('generate-btn', 'disabled')],
        prevent_initial_call=True
    )
    def handle_generate(n_clicks, btn_disabled):
        """
        Handle README generation
        """
        if upload_callbacks.parsed_project_data is None:
            return (
                "",
                "No project uploaded",
                "status-indicator",
                dbc.Toast("Please upload a ZIP file first.", header="Upload Required", icon="warning", duration=3000)
            )
        
        # Check if Gemini is configured
        if not gemini_service.is_configured():
            error_msg = gemini_service.get_error() or "Gemini API not configured"
            return (
                "",
                f"Error: {error_msg}",
                "status-indicator error",
                dbc.Toast(f"Gemini Config Error: {error_msg}", header="Configuration Error", icon="danger", duration=4000)
            )
        
        try:
            # Generate README using Gemini
            readme_content = gemini_service.generate_readme(upload_callbacks.parsed_project_data)
            
            # Update status to completed
            status_text = "README Generated ✓"
            
            # Return updated content, status, and success Toast
            return (
                readme_content,
                status_text,
                "status-indicator completed",
                dbc.Toast("README file generated successfully using Groq AI!", header="Generation Complete", icon="success", duration=3000)
            )
        
        except Exception as e:
            error_message = f"Generation failed: {str(e)}"
            return (
                "",
                error_message,
                "status-indicator error",
                dbc.Toast(f"Generation failed: {str(e)}", header="Generation Failed", icon="danger", duration=4000)
            )
