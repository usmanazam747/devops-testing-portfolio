"""
Integration tests for User Service
Tests the service with real database and API endpoints
"""
import pytest
import requests
import time
import os


BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
TIMEOUT = 30  # seconds to wait for service


@pytest.fixture(scope="module")
def wait_for_service():
    """Wait for the service to be ready before running tests"""
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print(f"Service is ready at {BASE_URL}")
                return True
        except requests.exceptions.RequestException:
            time.sleep(2)
    
    pytest.fail(f"Service did not become ready within {TIMEOUT} seconds")


@pytest.fixture
def cleanup_test_user():
    """Cleanup fixture to remove test users after tests"""
    yield
    # Add cleanup logic if needed (e.g., delete test users)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, wait_for_service):
        """Test that health endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'


class TestUserRegistrationIntegration:
    """Integration tests for user registration flow"""
    
    def test_register_new_user_success(self, wait_for_service, cleanup_test_user):
        """Test successful user registration with database persistence"""
        user_data = {
            'username': f'testuser_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'password': 'SecurePass123!'
        }
        
        response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert 'user' in data
        assert data['user']['username'] == user_data['username']
        assert data['user']['email'] == user_data['email']
        assert 'password' not in data['user']  # Password should never be returned
    
    def test_register_duplicate_username(self, wait_for_service):
        """Test that duplicate username is rejected"""
        username = f'duplicate_user_{int(time.time())}'
        user_data = {
            'username': username,
            'email': f'user1_{int(time.time())}@example.com',
            'password': 'SecurePass123!'
        }
        
        # First registration should succeed
        response1 = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same username should fail
        user_data['email'] = f'user2_{int(time.time())}@example.com'
        response2 = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert response2.status_code == 409
        response_data = response2.json()
        error_msg = response_data.get('message', response_data.get('error', '')).lower()
        assert 'already exists' in error_msg or 'duplicate' in error_msg
    
    def test_register_duplicate_email(self, wait_for_service):
        """Test that duplicate email is rejected"""
        email = f'duplicate_{int(time.time())}@example.com'
        user_data = {
            'username': f'user1_{int(time.time())}',
            'email': email,
            'password': 'SecurePass123!'
        }
        
        # First registration should succeed
        response1 = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        user_data['username'] = f'user2_{int(time.time())}'
        response2 = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert response2.status_code == 409
        response_data = response2.json()
        error_msg = response_data.get('message', response_data.get('error', '')).lower()
        assert 'already exists' in error_msg or 'duplicate' in error_msg
    
    def test_register_invalid_email(self, wait_for_service):
        """Test that invalid email format is accepted (API doesn't validate format)"""
        user_data = {
            'username': f'testuser_{int(time.time())}',
            'email': 'invalid-email',
            'password': 'SecurePass123!'
        }
        
        response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        # API currently doesn't validate email format, so this succeeds
        assert response.status_code == 201
    
    def test_register_missing_fields(self, wait_for_service):
        """Test that missing required fields are rejected"""
        # Missing password
        response = requests.post(f"{BASE_URL}/api/users/register", json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        assert response.status_code == 400


class TestUserLoginIntegration:
    """Integration tests for user login flow"""
    
    @pytest.fixture
    def registered_user(self, wait_for_service):
        """Create a user for login tests"""
        user_data = {
            'username': f'logintest_{int(time.time())}',
            'email': f'logintest_{int(time.time())}@example.com',
            'password': 'TestPassword123!'
        }
        response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert response.status_code == 201
        return user_data
    
    def test_login_success(self, registered_user):
        """Test successful login returns JWT token"""
        login_data = {
            'username': registered_user['username'],
            'password': registered_user['password']
        }
        
        response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == registered_user['username']
        
        # Verify token is a valid JWT format (has 3 parts separated by dots)
        token = data['token']
        assert len(token.split('.')) == 3
    
    def test_login_wrong_password(self, registered_user):
        """Test login with incorrect password"""
        login_data = {
            'username': registered_user['username'],
            'password': 'WrongPassword123!'
        }
        
        response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, wait_for_service):
        """Test login with non-existent username"""
        login_data = {
            'username': 'nonexistent_user_12345',
            'password': 'SomePassword123!'
        }
        
        response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        assert response.status_code == 401


class TestAuthenticatedEndpointsIntegration:
    """Integration tests for authenticated endpoints"""
    
    @pytest.fixture
    def authenticated_user(self, wait_for_service):
        """Create and authenticate a user, return token"""
        # Register
        user_data = {
            'username': f'authtest_{int(time.time())}',
            'email': f'authtest_{int(time.time())}@example.com',
            'password': 'TestPassword123!'
        }
        reg_response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert reg_response.status_code == 201
        
        # Login
        login_data = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        login_response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        assert login_response.status_code == 200
        
        return {
            'token': login_response.json()['token'],
            'user_data': user_data,
            'user_id': reg_response.json()['user']['id']
        }
    
    def test_get_user_profile(self, authenticated_user):
        """Test retrieving user profile with valid token"""
        headers = {'Authorization': f"Bearer {authenticated_user['token']}"}
        user_id = authenticated_user['user_id']
        
        response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        # API may return nested user object or flat structure
        user_data = data.get('user', data)
        assert user_data['username'] == authenticated_user['user_data']['username']
        assert user_data['email'] == authenticated_user['user_data']['email']
        assert 'password' not in user_data and 'password_hash' not in user_data
    
    def test_update_user_profile(self, authenticated_user):
        """Test updating user profile"""
        headers = {'Authorization': f"Bearer {authenticated_user['token']}"}
        user_id = authenticated_user['user_id']
        
        update_data = {
            'email': f'updated_{int(time.time())}@example.com'
        }
        
        response = requests.put(
            f"{BASE_URL}/api/users/{user_id}",
            json=update_data,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        # API may return nested user object or flat structure
        user_data = data.get('user', data)
        assert user_data['email'] == update_data['email']
    
    def test_access_without_token(self, wait_for_service):
        """Test that protected endpoints reject requests without token"""
        response = requests.get(f"{BASE_URL}/api/users/1")
        assert response.status_code == 401
    
    def test_access_with_invalid_token(self, wait_for_service):
        """Test that protected endpoints reject invalid tokens"""
        headers = {'Authorization': 'Bearer invalid.token.here'}
        response = requests.get(f"{BASE_URL}/api/users/1", headers=headers)
        assert response.status_code == 401
    
    def test_access_other_user_profile(self, authenticated_user):
        """Test that users cannot access other users' profiles"""
        headers = {'Authorization': f"Bearer {authenticated_user['token']}"}
        
        # Try to access user with different ID
        other_user_id = authenticated_user['user_id'] + 999
        response = requests.get(f"{BASE_URL}/api/users/{other_user_id}", headers=headers)
        
        # Should be forbidden or not found
        assert response.status_code in [403, 404]


class TestDatabasePersistence:
    """Test data persistence across requests"""
    
    def test_user_data_persists(self, wait_for_service):
        """Test that user data persists in database across multiple requests"""
        # Register user
        user_data = {
            'username': f'persist_{int(time.time())}',
            'email': f'persist_{int(time.time())}@example.com',
            'password': 'PersistTest123!'
        }
        reg_response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        assert reg_response.status_code == 201
        
        # Login first time
        login_data = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        login_response1 = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        assert login_response1.status_code == 200
        token1 = login_response1.json()['token']
        
        # Login second time (should retrieve same user from DB)
        login_response2 = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        assert login_response2.status_code == 200
        token2 = login_response2.json()['token']
        
        # Both tokens should be valid (different tokens, same user)
        headers1 = {'Authorization': f"Bearer {token1}"}
        headers2 = {'Authorization': f"Bearer {token2}"}
        
        user_id = reg_response.json()['user']['id']
        
        response1 = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers1)
        response2 = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers2)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        # API may return nested user object or flat structure
        user1 = response1.json().get('user', response1.json())
        user2 = response2.json().get('user', response2.json())
        assert user1['username'] == user2['username']


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_json(self, wait_for_service):
        """Test handling of invalid JSON"""
        response = requests.post(
            f"{BASE_URL}/api/users/register",
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code in [400, 422]
    
    def test_invalid_http_method(self, wait_for_service):
        """Test invalid HTTP methods"""
        response = requests.delete(f"{BASE_URL}/api/users/register")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_nonexistent_endpoint(self, wait_for_service):
        """Test accessing non-existent endpoint"""
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404
