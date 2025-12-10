"""
Authentication routes: Register, Login, Get Current User
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from app import mongo
from app.models import User
from app.utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Missing required fields: email, password, name'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()
        
        # Check if user already exists
        try:
            existing_user = mongo.db.users.find_one({'email': email})
        except Exception as db_error:
            current_app.logger.error(f"Database error during registration check: {str(db_error)}")
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Hash password and create user
        try:
            password_hash = hash_password(password)
        except Exception as hash_error:
            current_app.logger.error(f"Password hashing error: {str(hash_error)}")
            return jsonify({'error': 'Registration failed. Please try again.'}), 500
        
        user_doc = User.create_user(email, password_hash, name)
        
        # Insert user into database
        try:
            result = mongo.db.users.insert_one(user_doc)
            user_id = str(result.inserted_id)
        except Exception as insert_error:
            current_app.logger.error(f"Database insert error: {str(insert_error)}")
            return jsonify({'error': 'Failed to create user. Please try again.'}), 500
        
        # Generate JWT token
        try:
            access_token = create_access_token(identity=user_id)
        except Exception as jwt_error:
            current_app.logger.error(f"JWT token generation error: {str(jwt_error)}")
            return jsonify({'error': 'Registration failed. Please try again.'}), 500
        
        current_app.logger.info(f"Successful registration for user: {email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'email': email,
                'name': name,
                'has_preferences': False
            }
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login existing user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        try:
            user = mongo.db.users.find_one({'email': email})
        except Exception as db_error:
            current_app.logger.error(f"Database error during login: {str(db_error)}")
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        
        if not user:
            current_app.logger.warning(f"Login attempt with non-existent email: {email}")
            return jsonify({'error': 'The username or password is incorrect.'}), 401
        
        # Verify password
        try:
            password_valid = verify_password(password, user['password_hash'])
        except Exception as pwd_error:
            current_app.logger.error(f"Password verification error: {str(pwd_error)}")
            return jsonify({'error': 'The username or password is incorrect.'}), 401
        
        if not password_valid:
            current_app.logger.warning(f"Invalid password attempt for email: {email}")
            return jsonify({'error': 'The username or password is incorrect.'}), 401
        
        # Generate JWT token
        user_id = str(user['_id'])
        access_token = create_access_token(identity=user_id)
        
        current_app.logger.info(f"Successful login for user: {email}")
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'email': user['email'],
                'name': user['name'],
                'has_preferences': user.get('preferences') is not None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info"""
    try:
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['name'],
                'has_preferences': user.get('preferences') is not None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

