"""
================================================================================
 LLM SERVICE
--------------------------------------------------------------------------------
 Single responsibility: build the chat model used for answer generation.
 Supports Google Gemini, OpenAI, Anthropic, and local Llama via Ollama -
 swap providers with LLM_PROVIDER in .env, nothing else in the app needs
 to change.
================================================================================
"""

from functools import lru_cache
import config


@lru_cache(maxsize=1)
def get_llm():
    """Return one shared chat-model instance for the configured provider."""

    if config.LLM_PROVIDER == "ollama":
        # Fully local Llama model - no API key, no internet call at
        # inference time. Requires Ollama running locally (ollama.com)
        # with the model already pulled, e.g.: `ollama pull llama3.1`
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=config.OLLAMA_MODEL_NAME,
            base_url=config.OLLAMA_BASE_URL,
            temperature=config.LLM_TEMPERATURE,
        )

    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL_NAME,
            google_api_key=config.GEMINI_API_KEY,
            temperature=config.LLM_TEMPERATURE,
        )

    if config.LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL_NAME,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=config.LLM_TEMPERATURE,
        )

    # default: openai
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=config.OPENAI_MODEL_NAME,
        api_key=config.OPENAI_API_KEY,
        temperature=config.LLM_TEMPERATURE,
    )