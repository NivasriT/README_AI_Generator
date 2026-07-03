"""
Upload Callbacks for AI README Generator
Handles file upload events and ZIP extraction
"""

from dash import Input, Output, State, html, ctx
import dash_bootstrap_components as dbc
from services.zip_service import ZipService
from services.parser_service import ParserService

# Global service instances
zip_service = ZipService()
parser_service = ParserService()

# Global storage for extracted and parsed project data
extracted_project_data = None
parsed_project_data = None


def register_upload_callbacks(app):
    """
    Register upload-related callbacks with the Dash app
    """
    
    @app.callback(
        [Output('upload-filename', 'children'),
         Output('status-text', 'children'),
         Output('status-indicator', 'className'),
         Output('generate-btn', 'disabled'),
         Output('notification-container', 'children', allow_duplicate=True)],
        [Input('upload-zip', 'contents')],
        [State('upload-zip', 'filename')],
        prevent_initial_call=True
    )
    def handle_upload(contents, filename):
        """
        Handle ZIP file upload
        """
        global extracted_project_data, parsed_project_data
        
        if contents is None:
            return "", "No Project Uploaded", "status-indicator", True, None
        
        if not filename or not filename.lower().endswith('.zip'):
            return (
                "",
                "Invalid file format. Please upload a .zip file.",
                "status-indicator error",
                True,
                dbc.Toast("Please upload a .zip file format, other formats are not supported.", header="Format Error", icon="warning", duration=3000)
            )
        
        try:
            # Extract ZIP file
            extracted_files, metadata = zip_service.extract_zip(contents, filename)
            
            # Store extracted data globally
            extracted_project_data = {
                'files': extracted_files,
                'metadata': metadata
            }
            
            # Parse the project
            parsed_project_data = parser_service.parse_project(extracted_files)
            
            # Build success message
            file_count = metadata['file_count']
            ignored_count = metadata['ignored_count']
            project_name = metadata['project_name']
            
            success_message = f"✓ {project_name}"
            
            # Build status text
            status_text = f"Ready • {file_count} files extracted"
            if ignored_count > 0:
                status_text += f" ({ignored_count} ignored)"
            
            return (
                success_message,
                status_text,
                "status-indicator ready",
                False,
                dbc.Toast(f"Successfully uploaded and parsed '{project_name}'. Ready to generate!", header="Upload Successful", icon="success", duration=3000)
            )
        
        except Exception as e:
            error_message = f"Upload failed: {str(e)}"
            extracted_project_data = None
            parsed_project_data = None
            return (
                "",
                error_message,
                "status-indicator error",
                True,
                dbc.Toast(f"Upload failed: {str(e)}", header="Upload Failed", icon="danger", duration=4000)
            )
