"""
ZIP Service for AI README Generator
Handles ZIP file extraction and in-memory operations
"""

import zipfile
import io
import base64
import os
import tempfile
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ZipService:
    """Service for handling ZIP file operations"""
    
    # Binary and media file extensions to ignore
    IGNORED_EXTENSIONS = {
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
        # Videos
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
        # Audio
        '.mp3', '.wav', '.ogg', '.flac', '.aac',
        # Archives
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
        # Executables
        '.exe', '.dll', '.so', '.dylib', '.app', '.bin',
        # Fonts
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        # Other binary files
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.psd', '.ai', '.sketch', '.fig'
    }
    
    # Important file names to prioritize
    IMPORTANT_FILES = [
        'README.md', 'README.txt', 'README.rst', 'README',
        'package.json', 'package-lock.json', 'yarn.lock',
        'requirements.txt', 'setup.py', 'pyproject.toml',
        'Cargo.toml', 'Cargo.lock',
        'go.mod', 'go.sum',
        'pom.xml', 'build.gradle',
        'Gemfile', 'Gemfile.lock',
        'composer.json', 'composer.lock',
        '.gitignore', '.env.example', 'dockerfile', 'docker-compose.yml'
    ]
    
    def __init__(self):
        self.extracted_files = {}
        self.temp_dir = None
    
    def extract_zip(self, zip_content: str, filename: str) -> Tuple[Dict[str, bytes], Dict]:
        """
        Extract ZIP file content in memory
        
        Args:
            zip_content: Base64 encoded ZIP content
            filename: Original filename of the uploaded ZIP
            
        Returns:
            Tuple of (extracted_files dict, metadata dict)
        """
        # Decode base64 content
        if ',' in zip_content:
            zip_content = zip_content.split(',')[1]
        
        zip_data = base64.b64decode(zip_content)
        
        # Create temporary directory for extraction
        self.temp_dir = tempfile.mkdtemp(prefix='readme_gen_')
        
        extracted_files = {}
        file_count = 0
        ignored_count = 0
        
        try:
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    # Skip directories
                    if file_info.is_dir():
                        continue
                    
                    file_path = file_info.filename
                    file_ext = Path(file_path).suffix.lower()
                    
                    # Skip binary and media files
                    if file_ext in self.IGNORED_EXTENSIONS:
                        ignored_count += 1
                        continue
                    
                    # Skip very large files (> 1MB)
                    if file_info.file_size > 1024 * 1024:
                        ignored_count += 1
                        continue
                    
                    # Extract file content
                    try:
                        content = zip_ref.read(file_info.filename)
                        extracted_files[file_path] = content
                        file_count += 1
                    except Exception as e:
                        # Skip files that can't be read
                        ignored_count += 1
                        continue
        
        except Exception as e:
            raise Exception(f"Failed to extract ZIP file: {str(e)}")
        
        self.extracted_files = extracted_files
        
        # Generate metadata
        project_name = self._extract_project_name(filename)
        file_structure = self.get_file_structure(extracted_files)
        important_files = self.get_important_files(extracted_files)
        
        metadata = {
            'project_name': project_name,
            'file_count': file_count,
            'ignored_count': ignored_count,
            'file_structure': file_structure,
            'important_files': list(important_files.keys()),
            'total_size': sum(len(content) for content in extracted_files.values())
        }
        
        return extracted_files, metadata
    
    def _extract_project_name(self, filename: str) -> str:
        """
        Extract project name from ZIP filename
        
        Args:
            filename: Original ZIP filename
            
        Returns:
            Project name
        """
        # Remove .zip extension
        name = filename.replace('.zip', '').replace('.ZIP', '')
        # Remove any path components
        name = os.path.basename(name)
        return name
    
    def get_file_structure(self, extracted_files: Dict[str, bytes]) -> List[str]:
        """
        Get folder structure from extracted files
        
        Args:
            extracted_files: Dictionary of extracted files
            
        Returns:
            List of file paths representing the structure
        """
        if not extracted_files:
            return []
        
        # Get unique file paths
        file_paths = sorted(extracted_files.keys())
        
        # Build folder hierarchy
        structure = []
        for path in file_paths:
            parts = path.split('/')
            for i in range(len(parts)):
                subpath = '/'.join(parts[:i+1])
                if subpath not in structure:
                    structure.append(subpath)
        
        return structure
    
    def get_important_files(self, extracted_files: Dict[str, bytes]) -> Dict[str, bytes]:
        """
        Identify and return important files (README, package.json, etc.)
        
        Args:
            extracted_files: Dictionary of extracted files
            
        Returns:
            Dictionary of important files
        """
        important = {}
        
        for file_path, content in extracted_files.items():
            filename = os.path.basename(file_path).lower()
            
            # Check if file is in important list
            for important_file in self.IMPORTANT_FILES:
                if filename == important_file.lower():
                    important[file_path] = content
                    break
        
        return important
    
    def cleanup(self):
        """
        Clean up temporary directory and extracted files
        """
        self.extracted_files = {}
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """
        Get decoded content of a specific file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Decoded file content as string, or None if not found
        """
        if file_path not in self.extracted_files:
            return None
        
        try:
            return self.extracted_files[file_path].decode('utf-8')
        except UnicodeDecodeError:
            return None
