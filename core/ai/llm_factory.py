"""
LLM Factory Module
Factory pattern for creating LLM clients based on provider configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from .base_llm import BaseLLMClient
from .groq_client import GroqClient

load_dotenv()


class LLMFactory:
    """
    Factory class for creating LLM clients based on provider configuration.
    Supports easy addition of new LLM providers.
    """
    
    _providers = {
        "groq": GroqClient,
        # Future providers can be added here:
        # "gemini": GeminiClient,
        # "openai": OpenAIClient,
        # "claude": ClaudeClient,
        # "openrouter": OpenRouterClient,
    }
    
    @classmethod
    def create(
        cls,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> BaseLLMClient:
        """
        Create an LLM client based on the specified provider.
        
        Args:
            provider: LLM provider name (groq, gemini, openai, etc.).
                      If not provided, reads from AI_PROVIDER environment variable.
            api_key: API key for the provider. If not provided, reads from environment.
            model: Model name. If not provided, reads from environment.
            
        Returns:
            BaseLLMClient instance for the specified provider.
            
        Raises:
            ValueError: If provider is not supported or configuration is invalid.
        """
        # Get provider from environment if not specified
        if not provider:
            provider = os.getenv("AI_PROVIDER", "groq")
        
        provider = provider.lower()
        
        # Check if provider is supported
        if provider not in cls._providers:
            supported = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {supported}"
            )
        
        # Get the client class
        client_class = cls._providers[provider]
        
        # Create and return the client instance
        try:
            return client_class(api_key=api_key, model=model)
        except Exception as e:
            raise ValueError(
                f"Failed to create {provider} client: {str(e)}"
            )
    
    @classmethod
    def register_provider(cls, name: str, client_class: type) -> None:
        """
        Register a new LLM provider.
        
        Args:
            name: Provider name (lowercase).
            client_class: Client class that inherits from BaseLLMClient.
        """
        if not issubclass(client_class, BaseLLMClient):
            raise ValueError(
                f"Client class must inherit from BaseLLMClient"
            )
        
        cls._providers[name.lower()] = client_class
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Get list of supported LLM providers.
        
        Returns:
            List of provider names.
        """
        return list(cls._providers.keys())
