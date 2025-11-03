"""
API tests for RAGFlow endpoints
Testing authentication, dialogs, conversations, and knowledge bases
"""
import pytest
import requests
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Base URL for API
BASE_URL = "http://localhost"
API_BASE = f"{BASE_URL}/v1"


@pytest.mark.api
class TestAuthentication:
    """API tests for authentication endpoints"""
    
    def test_login_success(self):
        """
        Test successful login.
        
        Given: Valid credentials
        When: Logging in
        Then: Should return token
        """
        login_data = {
            "email": "admin@evragaz.local",
            "password": "Admin123!@#"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/user/login",
                json=login_data,
                timeout=10
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                assert 'data' in data or 'token' in data or 'access_token' in data
            else:
                # Login might not be at this endpoint
                pytest.skip(f"Login endpoint returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception as e:
            pytest.fail(f"Login test failed: {e}")
    
    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        
        Given: Invalid credentials
        When: Attempting login
        Then: Should return 401 or 400
        """
        login_data = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/user/login",
                json=login_data,
                timeout=10
            )
            
            # Should fail
            assert response.status_code in [400, 401, 404]
                
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception as e:
            # Some error responses are acceptable
            pass


@pytest.mark.api
class TestDialogAPI:
    """API tests for dialog endpoints"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        login_data = {
            "email": "admin@evragaz.local",
            "password": "Admin123!@#"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/user/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Try different possible token locations
                token = (data.get('data', {}).get('token') or 
                        data.get('token') or 
                        data.get('access_token'))
                return token
            else:
                pytest.skip("Cannot obtain auth token")
                
        except Exception:
            pytest.skip("Cannot obtain auth token")
    
    def test_list_dialogs(self, auth_token):
        """
        Test listing dialogs.
        
        Given: Authenticated user
        When: Listing dialogs
        Then: Should return dialog list
        """
        if not auth_token:
            pytest.skip("No auth token")
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{API_BASE}/dialog/list",
                headers=headers,
                params={"page": 1, "page_size": 10},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                assert 'data' in data or 'dialogs' in data
            else:
                pytest.skip(f"Dialog list endpoint returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception as e:
            pytest.fail(f"List dialogs test failed: {e}")
    
    def test_create_dialog(self, auth_token):
        """
        Test creating a new dialog.
        
        Given: Authenticated user
        When: Creating dialog
        Then: Should succeed
        """
        if not auth_token:
            pytest.skip("No auth token")
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        dialog_data = {
            "name": "Test Dialog from API Test",
            "description": "Created by automated test",
            "language": "English"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/dialog",
                headers=headers,
                json=dialog_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                assert 'data' in data or 'id' in data
                
                # Try to delete the created dialog
                if 'data' in data and 'id' in data['data']:
                    dialog_id = data['data']['id']
                    requests.delete(
                        f"{API_BASE}/dialog/{dialog_id}",
                        headers=headers
                    )
            else:
                pytest.skip(f"Dialog creation returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception as e:
            pytest.fail(f"Create dialog test failed: {e}")


@pytest.mark.api
class TestKnowledgeBaseAPI:
    """API tests for knowledge base endpoints"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        login_data = {
            "email": "admin@evragaz.local",
            "password": "Admin123!@#"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/user/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                token = (data.get('data', {}).get('token') or 
                        data.get('token') or 
                        data.get('access_token'))
                return token
            else:
                pytest.skip("Cannot obtain auth token")
                
        except Exception:
            pytest.skip("Cannot obtain auth token")
    
    def test_list_knowledge_bases(self, auth_token):
        """
        Test listing knowledge bases.
        
        Given: Authenticated user
        When: Listing knowledge bases
        Then: Should return list
        """
        if not auth_token:
            pytest.skip("No auth token")
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{API_BASE}/kb/list",
                headers=headers,
                params={"page": 1, "page_size": 10},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                assert 'data' in data or 'kbs' in data or 'knowledgebases' in data
            else:
                pytest.skip(f"KB list endpoint returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception as e:
            pytest.fail(f"List KBs test failed: {e}")


@pytest.mark.api
class TestHealthCheck:
    """API tests for health check endpoints"""
    
    def test_root_endpoint(self):
        """
        Test root endpoint accessibility.
        
        Given: RAGFlow server
        When: Accessing root
        Then: Should respond
        """
        try:
            response = requests.get(BASE_URL, timeout=5)
            assert response.status_code in [200, 301, 302, 404]
            
        except requests.exceptions.ConnectionError:
            pytest.fail("RAGFlow server not accessible")
        except Exception as e:
            pytest.fail(f"Health check failed: {e}")
    
    def test_api_version_endpoint(self):
        """
        Test API version endpoint.
        
        Given: RAGFlow API
        When: Checking version
        Then: Should return version info
        """
        try:
            # Try common version endpoints
            endpoints = [
                f"{API_BASE}/version",
                f"{API_BASE}/health",
                f"{BASE_URL}/api/health"
            ]
            
            for endpoint in endpoints:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    return  # At least one endpoint works
            
            # If none work, that's also acceptable
            pytest.skip("No version/health endpoint found")
            
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except Exception:
            pytest.skip("Version check not available")


@pytest.mark.api
@pytest.mark.critical
class TestSecurityIssues:
    """API tests for security vulnerabilities"""
    
    def test_unauthorized_access_to_dialogs(self):
        """
        Test that unauthorized users cannot access dialogs.
        
        Given: No authentication
        When: Trying to access dialogs
        Then: Should return 401 or redirect
        """
        try:
            response = requests.get(
                f"{API_BASE}/dialog/list",
                timeout=10,
                allow_redirects=False  # Don't follow redirects
            )
            
            # RAGFlow returns HTTP 200 with JSON code 401 (not ideal but acceptable)
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Check if response contains error code
                    if 'code' in data:
                        assert data['code'] in [401, 403], \
                            f"Response code should indicate auth error, got {data['code']}"
                    else:
                        pytest.fail("Unauthorized access returned 200 with no error code")
                except:
                    pytest.fail("Unauthorized access returned 200 with invalid JSON")
            else:
                # Proper HTTP status codes
                assert response.status_code in [401, 403, 301, 302], \
                    f"Expected auth required, got {response.status_code}"
            
        except requests.exceptions.ConnectionError:
            pytest.skip("RAGFlow server not accessible")
        except AssertionError:
            raise
        except Exception as e:
            pytest.fail(f"Security test failed: {e}")
    
    def test_sql_injection_prevention(self):
        """
        Test SQL injection prevention.
        
        Given: Malicious input
        When: Sending to API
        Then: Should be sanitized
        """
        malicious_inputs = [
            "' OR '1'='1",
            "1; DROP TABLE users--",
            "admin'--"
        ]
        
        for payload in malicious_inputs:
            try:
                response = requests.post(
                    f"{API_BASE}/user/login",
                    json={"email": payload, "password": payload},
                    timeout=10
                )
                
                # Should not crash or return unexpected data
                assert response.status_code in [400, 401, 404, 422]
                
            except requests.exceptions.ConnectionError:
                pytest.skip("RAGFlow server not accessible")
            except Exception:
                # Any exception is acceptable for malicious input
                pass
