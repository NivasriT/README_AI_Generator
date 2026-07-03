"""
Parser Service for AI README Generator
Handles parsing of project files and extracting relevant information
"""

import json
import re
from typing import Dict, List, Optional, Any
from pathlib import Path


class ParserService:
    """Service for parsing project files"""
    
    # Important source files to detect
    IMPORTANT_SOURCE_FILES = [
        'app.py', 'main.py', 'index.js', 'index.ts', 'server.js', 'server.ts',
        '__init__.py', 'setup.py', 'manage.py', 'wsgi.py', 'asgi.py'
    ]
    
    # Configuration files to detect
    CONFIG_FILES = [
        'package.json', 'requirements.txt', 'pyproject.toml', 'Cargo.toml',
        'go.mod', 'pom.xml', 'build.gradle', 'Gemfile', 'composer.json',
        '.gitignore', '.env.example', 'dockerfile', 'docker-compose.yml',
        'tsconfig.json', 'webpack.config.js', 'vite.config.js', '.eslintrc',
        '.prettierrc', 'babel.config.js', 'jest.config.js'
    ]
    
    # Documentation files
    DOC_FILES = [
        'README.md', 'README.txt', 'README.rst', 'README',
        'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE', 'LICENSE.md',
        'AUTHORS', 'INSTALL.md', 'docs/'
    ]
    
    def __init__(self):
        pass
    
    def parse_project(self, extracted_files: Dict[str, bytes]) -> Dict[str, Any]:
        """
        Parse entire project and extract all relevant information
        
        Args:
            extracted_files: Dictionary of extracted files (path -> content)
            
        Returns:
            Structured dictionary with parsed project information
        """
        result = {
            'project_type': self.identify_project_type(extracted_files),
            'directory_tree': self.generate_directory_tree(extracted_files),
            'important_files': self.detect_important_files(extracted_files),
            'dependencies': self.extract_dependencies(extracted_files),
            'file_summaries': self.generate_file_summaries(extracted_files),
            'metadata': self.extract_metadata(extracted_files)
        }
        
        return result
    
    def identify_project_type(self, files: Dict[str, bytes]) -> str:
        """
        Identify project type based on files present
        
        Args:
            files: Dictionary of project files
            
        Returns:
            Project type (e.g., 'python', 'javascript', 'typescript', etc.)
        """
        file_paths = [path.lower() for path in files.keys()]
        
        # Check for Python
        if any('requirements.txt' in path or 'pyproject.toml' in path or 
               path.endswith('.py') for path in file_paths):
            return 'python'
        
        # Check for Node.js/JavaScript
        if any('package.json' in path or path.endswith('.js') for path in file_paths):
            # Check if TypeScript
            if any(path.endswith('.ts') or 'tsconfig.json' in path for path in file_paths):
                return 'typescript'
            return 'javascript'
        
        # Check for Go
        if any('go.mod' in path or path.endswith('.go') for path in file_paths):
            return 'go'
        
        # Check for Rust
        if any('cargo.toml' in path or path.endswith('.rs') for path in file_paths):
            return 'rust'
        
        # Check for Ruby
        if any('gemfile' in path or path.endswith('.rb') for path in file_paths):
            return 'ruby'
        
        # Check for Java
        if any('pom.xml' in path or 'build.gradle' in path or path.endswith('.java') 
               for path in file_paths):
            return 'java'
        
        # Check for PHP
        if any('composer.json' in path or path.endswith('.php') for path in file_paths):
            return 'php'
        
        # Check for Docker
        if any('dockerfile' in path or 'docker-compose' in path for path in file_paths):
            return 'docker'
        
        return 'unknown'
    
    def generate_directory_tree(self, files: Dict[str, bytes]) -> str:
        """
        Generate a clean directory tree representation
        
        Args:
            files: Dictionary of extracted files
            
        Returns:
            String representation of directory tree
        """
        if not files:
            return "Empty project"
        
        # Build tree structure
        tree = {}
        for path in files.keys():
            parts = path.split('/')
            current = tree
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = None  # File
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        
        # Convert to string representation
        return self._tree_to_string(tree)
    
    def _tree_to_string(self, tree: Dict, prefix: str = "", is_last: bool = True) -> str:
        """
        Convert tree dictionary to string representation
        
        Args:
            tree: Tree dictionary
            prefix: Current prefix for indentation
            is_last: Whether this is the last item at this level
            
        Returns:
            String representation
        """
        lines = []
        items = list(tree.keys())
        
        for i, (name, children) in enumerate(tree.items()):
            is_last_item = i == len(items) - 1
            connector = "└── " if is_last_item else "├── "
            lines.append(f"{prefix}{connector}{name}")
            
            if children is not None:
                extension = "    " if is_last_item else "│   "
                lines.append(self._tree_to_string(children, prefix + extension, is_last_item))
        
        return "\n".join(lines)
    
    def detect_important_files(self, files: Dict[str, bytes]) -> Dict[str, str]:
        """
        Detect and categorize important files
        
        Args:
            files: Dictionary of extracted files
            
        Returns:
            Dictionary mapping categories to file paths
        """
        important = {
            'source': [],
            'config': [],
            'docs': [],
            'readme': None
        }
        
        for path in files.keys():
            filename = path.lower()
            basename = Path(path).name.lower()
            
            # Check for source files
            if any(src in basename for src in self.IMPORTANT_SOURCE_FILES):
                important['source'].append(path)
            
            # Check for config files
            if any(config in filename for config in self.CONFIG_FILES):
                important['config'].append(path)
            
            # Check for documentation
            if any(doc in filename for doc in self.DOC_FILES):
                if 'readme' in filename:
                    important['readme'] = path
                else:
                    important['docs'].append(path)
        
        return important
    
    def extract_dependencies(self, files: Dict[str, bytes]) -> Dict[str, List[str]]:
        """
        Extract dependencies from configuration files
        
        Args:
            files: Dictionary of extracted files
            
        Returns:
            Dictionary mapping file types to dependency lists
        """
        dependencies = {}
        
        for path, content in files.items():
            filename = Path(path).name.lower()
            
            try:
                content_str = content.decode('utf-8', errors='ignore')
            except:
                continue
            
            if filename == 'package.json':
                dependencies['npm'] = self.parse_package_json(content_str)
            elif filename == 'requirements.txt':
                dependencies['python'] = self.parse_requirements_txt(content_str)
            elif filename == 'pyproject.toml':
                dependencies['python_poetry'] = self.parse_pyproject_toml(content_str)
            elif filename == 'cargo.toml':
                dependencies['rust'] = self.parse_cargo_toml(content_str)
            elif filename == 'go.mod':
                dependencies['go'] = self.parse_go_mod(content_str)
            elif filename == 'gemfile':
                dependencies['ruby'] = self.parse_gemfile(content_str)
        
        return dependencies
    
    def parse_package_json(self, content: str) -> List[str]:
        """
        Parse package.json file
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        try:
            data = json.loads(content)
            deps = []
            
            # Get dependencies
            if 'dependencies' in data:
                deps.extend(list(data['dependencies'].keys()))
            
            # Get dev dependencies
            if 'devDependencies' in data:
                deps.extend(list(data['devDependencies'].keys()))
            
            return deps
        except:
            return []
    
    def parse_requirements_txt(self, content: str) -> List[str]:
        """
        Parse requirements.txt file
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Extract package name (before version specifier)
                pkg = re.split(r'[<>=!~]', line)[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps
    
    def parse_pyproject_toml(self, content: str) -> List[str]:
        """
        Parse pyproject.toml file
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        deps = []
        # Simple TOML parsing for dependencies
        in_deps = False
        for line in content.split('\n'):
            line = line.strip()
            if '[project.dependencies]' in line or '[tool.poetry.dependencies]' in line:
                in_deps = True
                continue
            if in_deps and line.startswith('['):
                in_deps = False
                continue
            if in_deps and line and not line.startswith('#'):
                pkg = re.split(r'[<>=!~]', line.split('=')[0].strip())[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps
    
    def parse_cargo_toml(self, content: str) -> List[str]:
        """
        Parse Cargo.toml file
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        deps = []
        in_deps = False
        for line in content.split('\n'):
            line = line.strip()
            if '[dependencies]' in line:
                in_deps = True
                continue
            if in_deps and line.startswith('['):
                in_deps = False
                continue
            if in_deps and line and not line.startswith('#'):
                pkg = line.split('=')[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps
    
    def parse_go_mod(self, content: str) -> List[str]:
        """
        Parse go.mod file
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        deps = []
        in_require = False
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('require ('):
                in_require = True
                continue
            if in_require and line == ')':
                in_require = False
                continue
            if in_require and line and not line.startswith('//'):
                pkg = line.split()[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps
    
    def parse_gemfile(self, content: str) -> List[str]:
        """
        Parse Gemfile
        
        Args:
            content: File content as string
            
        Returns:
            List of dependencies
        """
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('gem '):
                # Extract gem name
                match = re.search(r'gem\s+["\']([^"\']+)["\']', line)
                if match:
                    deps.append(match.group(1))
        return deps
    
    def generate_file_summaries(self, files: Dict[str, bytes]) -> Dict[str, str]:
        """
        Generate concise summaries of key files
        
        Args:
            files: Dictionary of extracted files
            
        Returns:
            Dictionary mapping file paths to summaries
        """
        summaries = {}
        
        # Summarize important files
        for path, content in files.items():
            filename = Path(path).name.lower()
            
            # Only summarize important files
            if not any(important in filename for important in 
                      self.IMPORTANT_SOURCE_FILES + self.CONFIG_FILES + ['readme']):
                continue
            
            try:
                content_str = content.decode('utf-8', errors='ignore')
            except:
                summaries[path] = "[Binary file or unreadable]"
                continue
            
            # Generate summary based on file type
            if filename.endswith('.py'):
                summaries[path] = self._summarize_python_file(content_str)
            elif filename.endswith('.js') or filename.endswith('.ts'):
                summaries[path] = self._summarize_js_file(content_str)
            elif filename == 'package.json':
                summaries[path] = self._summarize_package_json(content_str)
            elif filename == 'requirements.txt':
                summaries[path] = self._summarize_requirements(content_str)
            elif 'readme' in filename:
                summaries[path] = self._summarize_readme(content_str)
            else:
                summaries[path] = self._summarize_generic_file(content_str)
        
        return summaries
    
    def _summarize_python_file(self, content: str) -> str:
        """Summarize Python file"""
        lines = content.split('\n')
        imports = []
        classes = []
        functions = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
            elif line.startswith('class '):
                classes.append(line)
            elif line.startswith('def '):
                functions.append(line)
        
        summary = f"Python file with {len(imports)} imports"
        if classes:
            summary += f", {len(classes)} classes"
        if functions:
            summary += f", {len(functions)} functions"
        return summary
    
    def _summarize_js_file(self, content: str) -> str:
        """Summarize JavaScript/TypeScript file"""
        lines = content.split('\n')
        imports = []
        functions = []
        
        for line in lines:
            line = line.strip()
            if 'import' in line or 'require' in line:
                imports.append(line)
            elif 'function' in line or '=>' in line:
                functions.append(line)
        
        summary = f"JS/TS file with {len(imports)} imports"
        if functions:
            summary += f", {len(functions)} functions"
        return summary
    
    def _summarize_package_json(self, content: str) -> str:
        """Summarize package.json"""
        try:
            data = json.loads(content)
            name = data.get('name', 'Unknown')
            version = data.get('version', 'Unknown')
            deps = len(data.get('dependencies', {}))
            dev_deps = len(data.get('devDependencies', {}))
            return f"Package: {name} v{version}, {deps} deps, {dev_deps} dev-deps"
        except:
            return "Invalid package.json"
    
    def _summarize_requirements(self, content: str) -> str:
        """Summarize requirements.txt"""
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        return f"Python requirements with {len(lines)} packages"
    
    def _summarize_readme(self, content: str) -> str:
        """Summarize README"""
        lines = content.split('\n')
        non_empty = [l for l in lines if l.strip()]
        return f"README with {len(non_empty)} lines"
    
    def _summarize_generic_file(self, content: str) -> str:
        """Summarize generic file"""
        lines = content.split('\n')
        return f"Configuration file with {len(lines)} lines"
    
    def extract_metadata(self, files: Dict[str, bytes]) -> Dict[str, Any]:
        """
        Extract project metadata
        
        Args:
            files: Dictionary of extracted files
            
        Returns:
            Dictionary with metadata
        """
        metadata = {
            'total_files': len(files),
            'total_size': sum(len(content) for content in files.values()),
            'file_types': self._count_file_types(files),
            'has_tests': self._has_tests(files),
            'has_ci': self._has_ci_config(files)
        }
        
        return metadata
    
    def _count_file_types(self, files: Dict[str, bytes]) -> Dict[str, int]:
        """Count files by extension"""
        types = {}
        for path in files.keys():
            ext = Path(path).suffix.lower()
            if ext:
                types[ext] = types.get(ext, 0) + 1
        return types
    
    def _has_tests(self, files: Dict[str, bytes]) -> bool:
        """Check if project has test files"""
        for path in files.keys():
            if 'test' in path.lower() or 'spec' in path.lower():
                return True
        return False
    
    def _has_ci_config(self, files: Dict[str, bytes]) -> bool:
        """Check if project has CI configuration"""
        ci_files = ['.github/', '.gitlab-ci.yml', '.travis.yml', 'jenkinsfile', 'circleci']
        for path in files.keys():
            if any(ci in path.lower() for ci in ci_files):
                return True
        return False
