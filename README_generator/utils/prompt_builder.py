"""
Prompt Builder for AI README Generator
Constructs structured prompts for Gemini AI based on parsed project data
"""

from typing import Dict, Any, List


class PromptBuilder:
    """Builder for structured AI prompts"""
    
    def __init__(self):
        pass
    
    def build_readme_prompt(self, parsed_project: Dict[str, Any]) -> str:
        """
        Build a comprehensive, structured prompt for README generation
        
        Args:
            parsed_project: Dictionary containing parsed project information
            
        Returns:
            Structured prompt string for Gemini AI
        """
        project_type = parsed_project.get('project_type', 'unknown')
        directory_tree = parsed_project.get('directory_tree', 'Empty project')
        important_files = parsed_project.get('important_files', {})
        dependencies = parsed_project.get('dependencies', {})
        file_summaries = parsed_project.get('file_summaries', {})
        metadata = parsed_project.get('metadata', {})
        
        # Build the prompt
        prompt = self._build_system_instructions()
        prompt += self._build_project_context(project_type, directory_tree, important_files, metadata)
        prompt += self._build_technologies_section(dependencies, file_summaries)
        prompt += self._build_output_requirements()
        prompt += self._build_anti_hallucination_rules()
        
        return prompt
    
    def _build_system_instructions(self) -> str:
        """
        Build system instructions for the AI
        
        Returns:
            System instruction string
        """
        return """You are an expert technical documentation writer specializing in creating professional README.md files for software projects. Your task is to generate a comprehensive, accurate, and well-structured README based on the provided project information.

"""
    
    def _build_project_context(self, project_type: str, directory_tree: str, 
                              important_files: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """
        Build project context section
        
        Args:
            project_type: Type of project (python, javascript, etc.)
            directory_tree: ASCII tree of project structure
            important_files: Dictionary of important file categories
            metadata: Project metadata
            
        Returns:
            Project context string
        """
        context = f"""PROJECT CONTEXT:
----------------
Project Type: {project_type.upper()}

PROJECT STRUCTURE:
```
{directory_tree}
```

IMPORTANT FILES:
"""
        
        # Add source files
        source_files = important_files.get('source', [])
        if source_files:
            context += f"\nSource Files:\n"
            for file in source_files[:10]:
                context += f"  - {file}\n"
        
        # Add configuration files
        config_files = important_files.get('config', [])
        if config_files:
            context += f"\nConfiguration Files:\n"
            for file in config_files[:10]:
                context += f"  - {file}\n"
        
        # Add documentation
        docs = important_files.get('docs', [])
        if docs:
            context += f"\nDocumentation:\n"
            for doc in docs[:5]:
                context += f"  - {doc}\n"
        
        # Add existing README if present
        existing_readme = important_files.get('readme')
        if existing_readme:
            context += f"\nExisting README: {existing_readme}\n"
        
        # Add metadata
        context += f"""
PROJECT METADATA:
- Total Files: {metadata.get('total_files', 0)}
- Total Size: {metadata.get('total_size', 0)} bytes
- Has Test Files: {'Yes' if metadata.get('has_tests') else 'No'}
- Has CI/CD Configuration: {'Yes' if metadata.get('has_ci') else 'No'}

"""
        
        return context
    
    def _build_technologies_section(self, dependencies: Dict[str, List[str]], 
                                   file_summaries: Dict[str, str]) -> str:
        """
        Build technologies and dependencies section
        
        Args:
            dependencies: Dictionary of dependencies by package manager
            file_summaries: File summaries
            
        Returns:
            Technologies section string
        """
        tech_section = """TECHNOLOGIES & DEPENDENCIES:
----------------------------
"""
        
        # Add dependencies by package manager
        if dependencies:
            for pkg_manager, deps in dependencies.items():
                if deps:
                    tech_section += f"\n{pkg_manager.upper()} Dependencies:\n"
                    # Show first 15 dependencies
                    for dep in deps[:15]:
                        tech_section += f"  - {dep}\n"
                    if len(deps) > 15:
                        tech_section += f"  ... and {len(deps) - 15} more\n"
        else:
            tech_section += "\nNo dependency files detected.\n"
        
        # Add key file summaries for additional context
        if file_summaries:
            tech_section += "\n\nKEY FILE ANALYSIS:\n"
            for file_path, summary in list(file_summaries.items())[:20]:
                tech_section += f"  {file_path}: {summary}\n"
        
        tech_section += "\n"
        
        return tech_section
    
    def _build_output_requirements(self) -> str:
        """
        Build output requirements section
        
        Returns:
            Output requirements string
        """
        return """REQUIRED README SECTIONS:
------------------------
Generate a README.md file with the following sections (in order):

1. **Project Title**
   - A clear, descriptive title for the project
   - Use the project name from the structure or a reasonable default
   - NO placeholder text like "Your Project Name"

2. **Description**
   - A concise 2-3 sentence description of what the project does
   - Mention the primary purpose and target users
   - Base this on the project type and files present

3. **Features**
   - List key features based on the actual files and dependencies
   - Only include features that are supported by the code structure
   - Use bullet points for clarity

4. **Folder Structure**
   - Include the actual project structure shown above
   - Use a code block with proper formatting
   - Briefly explain the purpose of key directories

5. **Technologies Used**
   - List all detected technologies and frameworks
   - Include the programming language and major dependencies
   - Group by category (e.g., Backend, Frontend, Testing)

6. **Installation**
   - Provide clear installation instructions
   - Include commands for the detected package manager
   - Add any prerequisites if applicable
   - Use code blocks for commands

7. **Usage**
   - Provide basic usage examples
   - Include code snippets if applicable
   - Explain how to run the application
   - Base examples on the detected entry points (main.py, index.js, etc.)

8. **Configuration**
   - If configuration files are present, explain key settings
   - Include environment variables if .env files are detected
   - Keep it concise and practical

9. **Contributing**
   - Brief guidelines for contributing
   - Include testing instructions if test files exist
   - Mention CI/CD if configured

10. **License**
    - If a LICENSE file exists, mention it
    - Otherwise, suggest a common license (MIT is a safe default)
    - Keep it brief

FORMATTING REQUIREMENTS:
-----------------------
- Use proper Markdown syntax throughout
- Use code blocks with language specification (e.g., ```bash, ```python, ```javascript)
- Use appropriate heading levels (# for title, ## for sections)
- Use bold for emphasis on key terms
- Use bullet points for lists
- Use tables where appropriate (e.g., for dependencies)
- Keep line length reasonable (under 100 characters)

"""
    
    def _build_anti_hallucination_rules(self) -> str:
        """
        Build anti-hallucination rules section
        
        Returns:
            Anti-hallucination rules string
        """
        return """CRITICAL RULES - DO NOT HALLUCINATE:
------------------------------------
1. ONLY include features that are supported by the actual project files
2. DO NOT invent features, commands, or configurations that don't exist
3. If uncertain about a feature, omit it rather than guess
4. Use the actual file names and paths from the project structure
5. Base installation instructions on the detected package manager
6. Only mention testing if test files are actually present
7. Only mention CI/CD if CI configuration files exist
8. Use real dependency names from the dependency lists
9. Do not include placeholder text like "your-api-key" or "your-database-url"
10. If information is missing, state it clearly or omit the section

ACCURACY GUIDELINES:
-------------------
- Be conservative: it's better to omit information than to be wrong
- Use the project type to make reasonable inferences, but stay grounded
- If the project has no clear purpose based on files, provide a generic description
- Installation commands must match the detected package manager
- Usage examples should be based on detected entry points

OUTPUT FORMAT:
-------------
Output ONLY the complete README.md content.
- Do not include any explanations or conversational text
- Do not include "Here is the README:" or similar prefixes
- Start directly with the project title
- End with the license section
- No additional text before or after the README

Generate the README.md now:
"""
    
    def build_section_prompt(self, section: str, context: Dict[str, Any]) -> str:
        """
        Build a prompt for generating a specific section
        
        Args:
            section: Section name (e.g., 'installation', 'usage')
            context: Context information
            
        Returns:
            Section-specific prompt
        """
        prompt = f"""Generate a professional {section.upper()} section for a README.md file.

Project Type: {context.get('project_type', 'unknown')}
Dependencies: {context.get('dependencies', [])}
Entry Points: {context.get('entry_points', [])}

REQUIREMENTS:
- Use proper Markdown formatting
- Include code blocks with appropriate language specification
- Be concise and practical
- Base content on the actual project information provided
- Do not hallucinate features or commands not supported by the project

Generate only the {section} section content:
"""
        
        return prompt
