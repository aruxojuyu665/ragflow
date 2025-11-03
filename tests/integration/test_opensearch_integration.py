"""
Integration tests for OpenSearch
Testing real connection, indexing, and k-NN search
"""
import pytest
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.integration
@pytest.mark.opensearch
class TestOpenSearchConnection:
    """Integration tests for OpenSearch connection"""
    
    def test_opensearch_is_running(self):
        """
        Test that OpenSearch is accessible.
        
        Given: OpenSearch service
        When: Connecting to localhost:9200
        Then: Should return cluster info
        """
        import requests
        
        try:
            response = requests.get('http://localhost:9200', timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert 'version' in data
            assert data['version']['distribution'] == 'opensearch'
            assert data['version']['number'].startswith('2.11')
            
        except Exception as e:
            pytest.fail(f"OpenSearch connection failed: {e}")
    
    def test_opensearch_cluster_health(self):
        """
        Test OpenSearch cluster health.
        
        Given: OpenSearch cluster
        When: Checking health
        Then: Should return status
        """
        import requests
        
        try:
            response = requests.get('http://localhost:9200/_cluster/health', timeout=5)
            assert response.status_code == 200
            
            health = response.json()
            assert 'status' in health
            assert health['status'] in ['green', 'yellow', 'red']
            
        except Exception as e:
            pytest.fail(f"Cluster health check failed: {e}")


@pytest.mark.integration
@pytest.mark.opensearch
@pytest.mark.slow
class TestOpenSearchIndexing:
    """Integration tests for OpenSearch indexing"""
    
    def test_create_test_index(self):
        """
        Test creating a test index.
        
        Given: OpenSearch connection
        When: Creating index with mapping
        Then: Should succeed
        """
        import requests
        
        index_name = "test_ragflow_integration"
        
        # Delete index if exists
        requests.delete(f'http://localhost:9200/{index_name}')
        
        # Create index with simple mapping
        mapping = {
            "settings": {
                "index.knn": True
            },
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "embedding_768_vec": {
                        "type": "knn_vector",
                        "dimension": 768
                    }
                }
            }
        }
        
        try:
            response = requests.put(
                f'http://localhost:9200/{index_name}',
                json=mapping,
                timeout=10
            )
            assert response.status_code == 200
            
            # Verify index exists
            response = requests.get(f'http://localhost:9200/{index_name}')
            assert response.status_code == 200
            
            # Cleanup
            requests.delete(f'http://localhost:9200/{index_name}')
            
        except Exception as e:
            pytest.fail(f"Index creation failed: {e}")
    
    def test_index_document_with_vector(self):
        """
        Test indexing document with embedding vector.
        
        Given: Test index
        When: Indexing document with vector
        Then: Should succeed
        """
        import requests
        
        index_name = "test_ragflow_vector"
        
        # Setup
        requests.delete(f'http://localhost:9200/{index_name}')
        
        mapping = {
            "settings": {"index.knn": True},
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "embedding_768_vec": {
                        "type": "knn_vector",
                        "dimension": 768
                    }
                }
            }
        }
        
        requests.put(f'http://localhost:9200/{index_name}', json=mapping)
        
        # Index document
        doc = {
            "content": "This is a test document",
            "embedding_768_vec": [0.1] * 768
        }
        
        try:
            response = requests.post(
                f'http://localhost:9200/{index_name}/_doc/doc1',
                json=doc,
                timeout=10
            )
            assert response.status_code in [200, 201]
            
            # Refresh index
            requests.post(f'http://localhost:9200/{index_name}/_refresh')
            
            # Verify document
            response = requests.get(f'http://localhost:9200/{index_name}/_doc/doc1')
            assert response.status_code == 200
            
            data = response.json()
            assert data['_source']['content'] == "This is a test document"
            
            # Cleanup
            requests.delete(f'http://localhost:9200/{index_name}')
            
        except Exception as e:
            pytest.fail(f"Document indexing failed: {e}")


@pytest.mark.integration
@pytest.mark.opensearch
@pytest.mark.slow
class TestOpenSearchKNNSearch:
    """Integration tests for k-NN vector search"""
    
    def test_knn_search_basic(self):
        """
        Test basic k-NN search.
        
        Given: Index with vector documents
        When: Performing k-NN search
        Then: Should return nearest neighbors
        """
        import requests
        
        index_name = "test_ragflow_knn"
        
        # Setup
        requests.delete(f'http://localhost:9200/{index_name}')
        
        mapping = {
            "settings": {"index.knn": True},
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "embedding_768_vec": {
                        "type": "knn_vector",
                        "dimension": 768
                    }
                }
            }
        }
        
        requests.put(f'http://localhost:9200/{index_name}', json=mapping)
        
        # Index multiple documents
        for i in range(5):
            doc = {
                "content": f"Document {i}",
                "embedding_768_vec": [0.1 * i] * 768
            }
            requests.post(
                f'http://localhost:9200/{index_name}/_doc/doc{i}',
                json=doc
            )
        
        # Refresh
        requests.post(f'http://localhost:9200/{index_name}/_refresh')
        
        # Perform k-NN search
        query = {
            "size": 3,
            "query": {
                "knn": {
                    "embedding_768_vec": {
                        "vector": [0.2] * 768,
                        "k": 3
                    }
                }
            }
        }
        
        try:
            response = requests.post(
                f'http://localhost:9200/{index_name}/_search',
                json=query,
                timeout=10
            )
            assert response.status_code == 200
            
            data = response.json()
            assert 'hits' in data
            assert len(data['hits']['hits']) <= 3
            
            # Cleanup
            requests.delete(f'http://localhost:9200/{index_name}')
            
        except Exception as e:
            pytest.fail(f"k-NN search failed: {e}")
    
    def test_knn_search_different_dimensions(self):
        """
        Test k-NN search with different vector dimensions.
        
        Given: Indexes with different dimensions
        When: Searching each
        Then: Should work for all dimensions
        """
        import requests
        
        dimensions = [512, 768, 1024, 1536, 3072]
        
        for dim in dimensions:
            index_name = f"test_knn_{dim}"
            
            # Setup
            requests.delete(f'http://localhost:9200/{index_name}')
            
            mapping = {
                "settings": {"index.knn": True},
                "mappings": {
                    "properties": {
                        f"embedding_{dim}_vec": {
                            "type": "knn_vector",
                            "dimension": dim
                        }
                    }
                }
            }
            
            requests.put(f'http://localhost:9200/{index_name}', json=mapping)
            
            # Index document
            doc = {f"embedding_{dim}_vec": [0.1] * dim}
            requests.post(f'http://localhost:9200/{index_name}/_doc/doc1', json=doc)
            requests.post(f'http://localhost:9200/{index_name}/_refresh')
            
            # Search
            query = {
                "size": 1,
                "query": {
                    "knn": {
                        f"embedding_{dim}_vec": {
                            "vector": [0.1] * dim,
                            "k": 1
                        }
                    }
                }
            }
            
            try:
                response = requests.post(
                    f'http://localhost:9200/{index_name}/_search',
                    json=query
                )
                assert response.status_code == 200
                
                # Cleanup
                requests.delete(f'http://localhost:9200/{index_name}')
                
            except Exception as e:
                pytest.fail(f"k-NN search failed for dimension {dim}: {e}")
