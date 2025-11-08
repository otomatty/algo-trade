"""
Proposal generator for algorithm proposals.

Related Documentation:
  ├─ Plan: docs/03_plans/algorithm-proposal/README.md
  └─ LLM Integration: docs/03_plans/llm-integration/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/algorithm_proposal/job_manager.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ uuid (standard library)
  ├─ src-python/modules/llm_integration.api_key_manager
  ├─ src-python/modules/llm_integration.openai_client
  ├─ src-python/modules/llm_integration.anthropic_client
  ├─ src-python/modules/llm_integration.prompt_builder
  ├─ src-python/modules/llm_integration.fallback_handler
  └─ src-python/modules/llm_integration.exceptions
"""
import logging
import uuid
from typing import Dict, Any, List, Optional

from modules.llm_integration.api_key_manager import APIKeyManager
from modules.llm_integration.openai_client import OpenAIClient
from modules.llm_integration.anthropic_client import AnthropicClient
from modules.llm_integration.prompt_builder import PromptBuilder
from modules.llm_integration.fallback_handler import FallbackHandler
from modules.llm_integration.exceptions import LLMError, ParseError


logger = logging.getLogger(__name__)


class ProposalGenerator:
    """Generates algorithm proposals using LLM."""
    
    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        api_key_manager: Optional[APIKeyManager] = None
    ):
        """
        Initialize proposal generator.
        
        Args:
            llm_provider: LLM provider name ("openai" or "anthropic")
            model: Model name (optional, uses default if not provided)
            api_key_manager: API key manager instance (optional)
        """
        self.api_key_manager = api_key_manager or APIKeyManager()
        self.llm_provider = llm_provider
        self.model = model
        self.llm_client = self._create_llm_client()
        self.prompt_builder = PromptBuilder()
        self.fallback_handler = FallbackHandler()
    
    def _create_llm_client(self):
        """Create LLM client based on provider."""
        if self.llm_provider == "openai":
            api_key = self.api_key_manager.get_openai_api_key()
            return OpenAIClient(api_key=api_key)
        elif self.llm_provider == "anthropic":
            api_key = self.api_key_manager.get_anthropic_api_key()
            return AnthropicClient(api_key=api_key)
        else:
            raise LLMError(f"Unknown LLM provider: {self.llm_provider}")
    
    def generate_proposals(
        self,
        analysis_result: Dict[str, Any],
        user_preferences: Optional[Dict[str, Any]] = None,
        num_proposals: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate algorithm proposals based on analysis results.
        
        Args:
            analysis_result: Analysis result dictionary
            user_preferences: User preferences dictionary (optional)
            num_proposals: Number of proposals to generate (default: 5)
            
        Returns:
            List of proposal dictionaries
            
        Raises:
            LLMError: If LLM API call fails
            ParseError: If response parsing fails
        """
        try:
            # Build prompt
            prompt = self.prompt_builder.build_algorithm_proposal_prompt(
                analysis_result,
                user_preferences,
                num_proposals
            )
            
            logger.info(f"Generating {num_proposals} algorithm proposals using {self.llm_provider}")
            
            # Call LLM API
            response_text = self.llm_client.generate(
                prompt,
                model=self.model,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response with fallback
            proposals = self.fallback_handler.parse_with_fallback(
                response_text,
                "algorithm_proposal"
            )
            
            # Add proposal IDs
            for proposal in proposals:
                if 'proposal_id' not in proposal:
                    proposal['proposal_id'] = str(uuid.uuid4())
            
            logger.info(f"Generated {len(proposals)} algorithm proposals")
            return proposals
            
        except LLMError as e:
            logger.error(f"LLM API error: {e}")
            raise
        except ParseError as e:
            logger.error(f"Parse error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in proposal generation: {e}")
            raise LLMError(f"Failed to generate proposals: {e}") from e

