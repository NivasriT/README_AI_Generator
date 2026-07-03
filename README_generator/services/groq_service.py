"""
Groq Service for AI README Generator
Handles integration with Groq AI API (free, fast, generous limits)
"""

from groq import Groq
from typing import Optional, Dict, Any
import os
import time
from dotenv import load_dotenv
from utils.prompt_builder import PromptBuilder


class GeminiService:
    """Service for Groq AI integration (drop-in replacement for Gemini)"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq service

        Args:
            api_key: Groq API key (defaults to environment variable)
        """
        load_dotenv()

        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.prompt_builder = PromptBuilder()
        self.model_name = 'llama-3.3-70b-versatile'

        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                self.model = True  # Flag that service is ready
            except Exception as e:
                self.client = None
                self.model = None
                self.error = f"Failed to initialize Groq: {str(e)}"
        else:
            self.client = None
            self.model = None
            self.error = "No API key provided. Set GROQ_API_KEY in .env file."

    def generate_readme(self, parsed_project: Dict[str, Any]) -> str:
        """
        Generate README content using Groq AI based on parsed project data

        Args:
            parsed_project: Dictionary containing parsed project information

        Returns:
            Generated README content as markdown
        """
        if not self.is_configured():
            raise ValueError(self.error or "Groq service is not configured")

        prompt = self.prompt_builder.build_readme_prompt(parsed_project)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert technical documentation writer. Generate professional, accurate README.md files based on project information provided."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                    top_p=0.9,
                )

                content = response.choices[0].message.content
                if content:
                    return content.strip()
                else:
                    raise Exception("Empty response from Groq API")

            except Exception as e:
                raw_error = str(e)
                error_lower = raw_error.lower()

                # Rate limit — retry with backoff
                if '429' in raw_error or 'rate_limit' in error_lower or 'rate limit' in error_lower:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                    raise Exception("Groq rate limit hit. Please wait a moment and try again.")

                # Auth errors
                elif '401' in raw_error or '403' in raw_error or 'invalid api key' in error_lower:
                    raise Exception("Invalid Groq API key. Please check GROQ_API_KEY in .env.")

                # Timeout
                elif 'timeout' in error_lower or 'deadline' in error_lower:
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    raise Exception("Request timed out. Please try again.")

                # All other errors — show the real message
                else:
                    raise Exception(f"Groq API error: {raw_error}")

    def generate_section(self, section: str, context: Dict[str, Any]) -> str:
        """
        Generate a specific README section using Groq AI
        """
        if not self.is_configured():
            raise ValueError(self.error or "Groq service is not configured")

        prompt = self.prompt_builder.build_section_prompt(section, context)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            raise Exception(f"Failed to generate {section} section: {str(e)}")

    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None and self.model is not None

    def get_error(self) -> Optional[str]:
        """Get the current error message if any"""
        return getattr(self, 'error', None)
