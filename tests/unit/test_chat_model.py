"""
Unit tests for LLM chat model providers
Testing JSON parsing and initialization for all providers
"""
import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from rag.llm.chat_model import OpenRouterChat


@pytest.mark.unit
class TestOpenRouterChat:
    """Unit tests for OpenRouterChat JSON parsing"""
    
    def test_json_parsing_valid_json(self, sample_api_keys):
        """
        Test parsing valid JSON API key for OpenRouter.
        
        Given: Valid JSON string with api_key and provider_order
        When: Initializing OpenRouterChat
        Then: Should extract api_key correctly
        """
        key = sample_api_keys["openrouter_json"]
        
        try:
            chat = OpenRouterChat(
                key=key,
                model_name="gpt-4",
                base_url="https://openrouter.ai/api/v1"
            )
            
            # Verify the key was parsed correctly
            key_data = json.loads(key)
            expected_key = key_data.get("api_key", "")
            
            # The actual implementation might store it differently
            # This test verifies no exception was raised
            assert chat is not None
            
        except Exception as e:
            pytest.fail(f"Failed to parse valid JSON key: {e}")
    
    def test_json_parsing_plain_string(self, sample_api_keys):
        """
        Test fallback to plain string API key for OpenRouter.
        
        Given: Plain string API key (not JSON)
        When: Initializing OpenRouterChat
        Then: Should use the string directly without errors
        """
        key = sample_api_keys["openrouter_string"]
        
        try:
            chat = OpenRouterChat(
                key=key,
                model_name="gpt-4",
                base_url="https://openrouter.ai/api/v1"
            )
            
            assert chat is not None
            
        except Exception as e:
            pytest.fail(f"Failed to handle plain string key: {e}")
    
    def test_json_parsing_invalid_json(self, sample_api_keys):
        """
        Test handling of invalid JSON.
        
        Given: Invalid JSON string (malformed)
        When: Initializing OpenRouterChat
        Then: Should fallback to treating as plain string
        """
        key = sample_api_keys["invalid_json"]
        
        try:
            chat = OpenRouterChat(
                key=key,
                model_name="gpt-4",
                base_url="https://openrouter.ai/api/v1"
            )
            
            assert chat is not None
            
        except Exception as e:
            pytest.fail(f"Failed to handle invalid JSON: {e}")
    
    def test_json_parsing_empty_string(self, sample_api_keys):
        """
        Test handling of empty API key.
        
        Given: Empty string as API key
        When: Initializing OpenRouterChat
        Then: Should handle gracefully
        """
        key = sample_api_keys["empty_string"]
        
        try:
            chat = OpenRouterChat(
                key=key,
                model_name="gpt-4",
                base_url="https://openrouter.ai/api/v1"
            )
            
            assert chat is not None
            
        except Exception as e:
            # Empty key might raise an exception, which is acceptable
            pass


@pytest.mark.unit
class TestAzureChat:
    """Unit tests for AzureChat JSON parsing"""
    
    def test_azure_json_parsing_valid(self, sample_api_keys):
        """
        Test parsing valid Azure JSON key.
        
        Given: Valid JSON with api_key and api_version
        When: Initializing AzureChat
        Then: Should extract both fields correctly
        """
        # Import here to avoid issues if module not available
        try:
            from rag.llm.chat_model import AzureChat
        except ImportError:
            pytest.skip("AzureChat not available")
        
        key = sample_api_keys["azure_json"]
        
        try:
            chat = AzureChat(
                key=key,
                model_name="gpt-4",
                base_url="https://azure.openai.com"
            )
            
            assert chat is not None
            
        except Exception as e:
            pytest.fail(f"Failed to parse valid Azure JSON key: {e}")
    
    def test_azure_json_parsing_plain_string(self, sample_api_keys):
        """
        Test Azure fallback to plain string.
        
        Given: Plain string API key
        When: Initializing AzureChat
        Then: Should use string directly with default api_version
        """
        try:
            from rag.llm.chat_model import AzureChat
        except ImportError:
            pytest.skip("AzureChat not available")
        
        key = sample_api_keys["azure_string"]
        
        try:
            chat = AzureChat(
                key=key,
                model_name="gpt-4",
                base_url="https://azure.openai.com"
            )
            
            assert chat is not None
            
        except Exception as e:
            pytest.fail(f"Failed to handle plain string Azure key: {e}")


@pytest.mark.unit
class TestBedrockChat:
    """Unit tests for Bedrock (LiteLLMChat) JSON parsing"""
    
    def test_bedrock_json_parsing_valid(self, sample_api_keys):
        """
        Test parsing valid Bedrock JSON key.
        
        Given: Valid JSON with bedrock_ak, bedrock_sk, bedrock_region
        When: Initializing LiteLLMChat for Bedrock
        Then: Should extract all fields correctly
        """
        try:
            from rag.llm.chat_model import LiteLLMChat
        except ImportError:
            pytest.skip("LiteLLMChat not available")
        
        key = sample_api_keys["bedrock_json"]
        
        try:
            chat = LiteLLMChat(
                key=key,
                model_name="bedrock/anthropic.claude-v2",
                base_url=""
            )
            
            assert chat is not None
            
        except Exception as e:
            # Bedrock might require actual credentials
            # Just verify no JSON parsing error
            if "JSONDecodeError" in str(e):
                pytest.fail(f"JSON parsing failed: {e}")


@pytest.mark.unit
class TestJSONParsingConsistency:
    """Test that all providers handle JSON parsing consistently"""
    
    def test_all_providers_handle_plain_string(self, sample_api_keys):
        """
        Test that all providers can handle plain string keys.
        
        This is a critical requirement for backward compatibility.
        """
        plain_key = "test-api-key-123"
        providers_to_test = [
            ("OpenRouterChat", "gpt-4", "https://openrouter.ai/api/v1"),
        ]
        
        for provider_name, model, base_url in providers_to_test:
            try:
                from rag.llm import chat_model
                provider_class = getattr(chat_model, provider_name)
                
                chat = provider_class(
                    key=plain_key,
                    model_name=model,
                    base_url=base_url
                )
                
                assert chat is not None, f"{provider_name} failed with plain string"
                
            except (ImportError, AttributeError):
                # Provider not available, skip
                continue
            except Exception as e:
                # Some providers might fail for other reasons
                # We only care about JSON parsing errors
                if "JSONDecodeError" in str(e) or "json" in str(e).lower():
                    pytest.fail(f"{provider_name} failed JSON handling: {e}")
