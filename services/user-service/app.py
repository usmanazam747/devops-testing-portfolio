from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/ecommerce')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secure SECRET_KEY handling
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if os.getenv('FLASK_ENV') == 'production':
        raise ValueError("SECRET_KEY environment variable must be set in production!")
    # Only for development/testing - NEVER use this in production!
    SECRET_KEY = 'dev-secret-key-unsafe-for-demo-only'
    print("⚠️  WARNING: Using insecure development secret key. Set SECRET_KEY env var for production!")

app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

# Middleware for JWT authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Routes
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'user-service'}), 200

@app.route('/api/users/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'User account is inactive'}), 403
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200

@app.route('/api/users/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current authenticated user"""
    return jsonify({'user': current_user.to_dict()}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """Update user information"""
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Update allowed fields
    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating user: {str(e)}'}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    """Deactivate user (soft delete)"""
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'User deactivated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deactivating user: {str(e)}'}), 500

@app.route('/api/users', methods=['GET'])
@token_required
def list_users(current_user):
    """List all users (admin functionality)"""
    users = User.query.filter_by(is_active=True).all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200

@app.route('/api/test/cleanup', methods=['DELETE'])
def cleanup_test_data():
    """Cleanup endpoint for testing - only available in non-production"""
    if os.getenv('FLASK_ENV') == 'production':
        return jsonify({'message': 'Not available in production'}), 403
    
    try:
        # Delete all users (for testing only)
        User.query.delete()
        db.session.commit()
        return jsonify({'message': 'Test data cleaned'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error cleaning data: {str(e)}'}), 500

# Database initialization - create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')
