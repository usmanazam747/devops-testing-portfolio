import pytest
import json
from app import app, db, User

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    # Register user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/api/users/register', 
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Login
    login_data = {
        'username': 'testuser',
        'password': 'TestPass123!'
    }
    response = client.post('/api/users/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    token = json.loads(response.data)['token']
    return {'Authorization': f'Bearer {token}'}

class TestHealthEndpoint:
    def test_health_check(self, client):
        """Test health endpoint returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'user-service'

class TestUserRegistration:
    def test_register_user_success(self, client):
        """Test successful user registration"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = client.post('/api/users/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'
        assert data['user']['username'] == 'newuser'
        assert data['user']['email'] == 'newuser@example.com'
        assert 'password' not in data['user']
    
    def test_register_user_missing_fields(self, client):
        """Test registration with missing required fields"""
        user_data = {
            'username': 'incomplete'
        }
        
        response = client.post('/api/users/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Missing required fields' in data['message']
    
    def test_register_duplicate_username(self, client):
        """Test registration with existing username"""
        user_data = {
            'username': 'duplicateuser',
            'email': 'first@example.com',
            'password': 'Pass123!'
        }
        
        # First registration
        client.post('/api/users/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Duplicate registration
        user_data['email'] = 'different@example.com'
        response = client.post('/api/users/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'Username already exists' in data['message']
    
    def test_register_duplicate_email(self, client):
        """Test registration with existing email"""
        user_data = {
            'username': 'user1',
            'email': 'duplicate@example.com',
            'password': 'Pass123!'
        }
        
        # First registration
        client.post('/api/users/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Duplicate email
        user_data['username'] = 'user2'
        response = client.post('/api/users/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'Email already exists' in data['message']

class TestUserLogin:
    def test_login_success(self, client):
        """Test successful login"""
        # Register user
        user_data = {
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'LoginPass123!'
        }
        client.post('/api/users/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Login
        login_data = {
            'username': 'loginuser',
            'password': 'LoginPass123!'
        }
        response = client.post('/api/users/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'
        assert 'token' in data
        assert data['user']['username'] == 'loginuser'
    
    def test_login_invalid_credentials(self, client):
        """Test login with wrong password"""
        # Register user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'CorrectPass123!'
        }
        client.post('/api/users/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Login with wrong password
        login_data = {
            'username': 'testuser',
            'password': 'WrongPass123!'
        }
        response = client.post('/api/users/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['message']
    
    def test_login_missing_credentials(self, client):
        """Test login without credentials"""
        response = client.post('/api/users/login',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Missing credentials' in data['message']
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent username"""
        login_data = {
            'username': 'nonexistent',
            'password': 'SomePass123!'
        }
        response = client.post('/api/users/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['message']

class TestAuthenticatedEndpoints:
    def test_get_current_user(self, client, auth_headers):
        """Test getting current authenticated user"""
        response = client.get('/api/users/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['username'] == 'testuser'
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get('/api/users/me')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Token is missing' in data['message']
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        headers = {'Authorization': 'Bearer invalid_token_here'}
        response = client.get('/api/users/me', headers=headers)
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid token' in data['message']
    
    def test_update_user(self, client, auth_headers):
        """Test updating user information"""
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = client.put('/api/users/1',
                             data=json.dumps(update_data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['first_name'] == 'Updated'
        assert data['user']['last_name'] == 'Name'
        assert data['user']['email'] == 'updated@example.com'
    
    def test_list_users(self, client, auth_headers):
        """Test listing all users"""
        response = client.get('/api/users', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert data['total'] >= 1
    
    def test_delete_user(self, client, auth_headers):
        """Test deactivating user"""
        response = client.delete('/api/users/1', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deactivated successfully' in data['message']

class TestUserModel:
    def test_user_model_creation(self, client):
        """Test User model creation"""
        with app.app_context():
            user = User(
                username='modeltest',
                email='model@example.com',
                first_name='Model',
                last_name='Test'
            )
            user.set_password('TestPass123!')
            
            assert user.username == 'modeltest'
            assert user.email == 'model@example.com'
            assert user.check_password('TestPass123!')
            assert not user.check_password('WrongPassword')
    
    def test_user_to_dict(self, client):
        """Test User model to_dict method"""
        with app.app_context():
            user = User(
                username='dicttest',
                email='dict@example.com',
                first_name='Dict',
                last_name='Test'
            )
            user.set_password('TestPass123!')
            
            user_dict = user.to_dict()
            
            assert 'username' in user_dict
            assert 'email' in user_dict
            assert 'password_hash' not in user_dict
            assert 'password' not in user_dict

# Pytest configuration for coverage
if __name__ == '__main__':
    pytest.main(['-v', '--cov=app', '--cov-report=html', '--cov-report=term'])
