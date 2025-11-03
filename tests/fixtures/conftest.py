"""
Test fixtures for EvRAGaz project
"""
import pytest
import json
from faker import Faker

fake = Faker()


@pytest.fixture
def sample_api_keys():
    """Sample API keys for testing LLM providers"""
    return {
        "openrouter_json": json.dumps({
            "api_key": "sk-or-v1-test-key",
            "provider_order": "openai,anthropic"
        }),
        "openrouter_string": "sk-or-v1-test-string",
        "azure_json": json.dumps({
            "api_key": "azure-test-key",
            "api_version": "2024-02-01"
        }),
        "azure_string": "azure-plain-key",
        "bedrock_json": json.dumps({
            "bedrock_ak": "AKIA-test",
            "bedrock_sk": "secret-key",
            "bedrock_region": "us-east-1"
        }),
        "invalid_json": '{"api_key": "test"',  # Missing closing brace
        "empty_string": "",
    }


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    return [
        {
            "id": "doc1",
            "content": "This is a test document about artificial intelligence.",
            "metadata": {"source": "test", "page": 1}
        },
        {
            "id": "doc2",
            "content": "Another document discussing machine learning concepts.",
            "metadata": {"source": "test", "page": 2}
        },
    ]


@pytest.fixture
def sample_embeddings():
    """Sample embedding vectors for testing"""
    return {
        "embedding_512": [0.1] * 512,
        "embedding_768": [0.2] * 768,
        "embedding_1024": [0.3] * 1024,
        "embedding_1536": [0.4] * 1536,
        "embedding_3072": [0.5] * 3072,
    }


@pytest.fixture
def mock_opensearch_response():
    """Mock OpenSearch search response"""
    return {
        "took": 5,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 2, "relation": "eq"},
            "max_score": 0.95,
            "hits": [
                {
                    "_index": "ragflow_test",
                    "_id": "doc1",
                    "_score": 0.95,
                    "_source": {
                        "content": "Test document",
                        "embedding_768_vec": [0.1] * 768
                    }
                },
                {
                    "_index": "ragflow_test",
                    "_id": "doc2",
                    "_score": 0.85,
                    "_source": {
                        "content": "Another document",
                        "embedding_768_vec": [0.2] * 768
                    }
                }
            ]
        }
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM completion response"""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a test response from the LLM."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }


@pytest.fixture
def sample_user_data():
    """Generate sample user data"""
    return {
        "email": fake.email(),
        "nickname": fake.user_name(),
        "password": fake.password(),
        "avatar": fake.image_url(),
    }


@pytest.fixture
def sample_tenant_data():
    """Generate sample tenant data"""
    return {
        "name": fake.company(),
        "llm_id": "openrouter/gpt-4",
        "embd_id": "openai/text-embedding-3-small",
        "asr_id": "openai/whisper-1",
        "img2txt_id": "openai/gpt-4-vision",
    }


@pytest.fixture
def sample_dialog_data():
    """Generate sample dialog data"""
    return {
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=200),
        "language": "English",
        "llm_id": "openrouter/gpt-4",
        "prompt": "You are a helpful assistant.",
    }


@pytest.fixture
def sample_kb_data():
    """Generate sample knowledge base data"""
    return {
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=200),
        "language": "English",
        "embd_id": "openai/text-embedding-3-small",
        "chunk_method": "naive",
    }
