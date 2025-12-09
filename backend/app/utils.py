"""
Utility functions for authentication and helpers
"""
import bcrypt
import hashlib
import json

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against a hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_content_hash(content):
    """Generate a unique hash for content to track feedback"""
    if isinstance(content, dict):
        content_str = json.dumps(content, sort_keys=True)
    else:
        content_str = str(content)
    return hashlib.sha256(content_str.encode('utf-8')).hexdigest()

