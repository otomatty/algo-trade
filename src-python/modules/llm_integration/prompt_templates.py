"""
Prompt template management for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Prompt Design: docs/03_plans/algorithm-proposal/llm-prompt-design.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/prompt_builder.py

Dependencies (External files that this file imports):
  ├─ pathlib (standard library)
  ├─ typing (standard library)
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
from pathlib import Path
from typing import Dict, Optional

from .exceptions import LLMError


logger = logging.getLogger(__name__)


class PromptTemplateManager:
    """Manages prompt templates for LLM integration."""
    
    # Template versions
    TEMPLATE_VERSIONS = {
        "algorithm_proposal": "1.0",
        "stock_prediction": "1.0",
    }
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize prompt template manager.
        
        Args:
            templates_dir: Directory containing template files (optional, defaults to module templates directory)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        self.templates_dir = templates_dir
        self._templates: Dict[str, str] = {}
    
    def load_template(self, template_name: str, version: Optional[str] = None) -> str:
        """
        Load a prompt template from file.
        
        Args:
            template_name: Name of the template (e.g., "algorithm_proposal")
            version: Template version (optional, uses default if not provided)
            
        Returns:
            Template content as string
            
        Raises:
            LLMError: If template file is not found or cannot be read
        """
        # Check cache first
        cache_key = f"{template_name}_{version or 'default'}"
        if cache_key in self._templates:
            return self._templates[cache_key]
        
        # Determine template file name
        if version:
            template_file = self.templates_dir / f"{template_name}_v{version}.txt"
        else:
            template_file = self.templates_dir / f"{template_name}.txt"
        
        if not template_file.exists():
            raise LLMError(f"Template file not found: {template_file}")
        
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                template_content = f.read()
            
            # Cache template
            self._templates[cache_key] = template_content
            logger.debug(f"Loaded template: {template_name} (version: {version or 'default'})")
            return template_content
            
        except Exception as e:
            raise LLMError(f"Failed to load template {template_name}: {e}") from e
    
    def get_template_version(self, template_name: str) -> str:
        """
        Get the default version for a template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Version string
        """
        return self.TEMPLATE_VERSIONS.get(template_name, "1.0")
    
    def validate_template(self, template_content: str, required_params: list) -> bool:
        """
        Validate that a template contains all required parameters.
        
        Args:
            template_content: Template content string
            required_params: List of required parameter names
            
        Returns:
            True if all required parameters are present
            
        Raises:
            LLMError: If required parameters are missing
        """
        missing_params = []
        for param in required_params:
            if f"{{{param}}}" not in template_content:
                missing_params.append(param)
        
        if missing_params:
            raise LLMError(f"Template missing required parameters: {missing_params}")
        
        return True
    
    def render_template(
        self,
        template_name: str,
        **kwargs
    ) -> str:
        """
        Load and render a template with provided parameters.
        
        Args:
            template_name: Name of the template
            **kwargs: Parameters to fill in the template
            
        Returns:
            Rendered template string
            
        Raises:
            LLMError: If template loading or rendering fails
        """
        template_content = self.load_template(template_name)
        
        try:
            return template_content.format(**kwargs)
        except KeyError as e:
            raise LLMError(f"Missing template parameter: {e}") from e
        except Exception as e:
            raise LLMError(f"Failed to render template: {e}") from e

