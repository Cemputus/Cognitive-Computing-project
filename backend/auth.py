"""
Authentication Module for Business Intelligence Analyst
Handles user authentication and authorization
"""

import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json
import os

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Sample users database (in production, use a real database)
SAMPLE_USERS = [
    {
        'id': '1',
        'email': 'admin@business.com',
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),  # Hashed password
        'name': 'Admin User',
        'role': 'admin',
        'created_at': '2024-01-01',
    },
    {
        'id': '2',
        'email': 'user1@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Sarah Nakato',
        'role': 'user',
        'created_at': '2024-01-15',
    },
    {
        'id': '3',
        'email': 'user2@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'James Mukasa',
        'role': 'user',
        'created_at': '2024-02-01',
    },
    {
        'id': '4',
        'email': 'user3@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Grace Namukasa',
        'role': 'user',
        'created_at': '2024-02-15',
    },
    {
        'id': '5',
        'email': 'user4@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'David Kato',
        'role': 'user',
        'created_at': '2024-03-01',
    },
    {
        'id': '6',
        'email': 'user5@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Mary Nalubega',
        'role': 'user',
        'created_at': '2024-03-15',
    },
    {
        'id': '7',
        'email': 'user6@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Peter Ssemwogerere',
        'role': 'user',
        'created_at': '2024-04-01',
    },
    {
        'id': '8',
        'email': 'user7@business.com',
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Ruth Nakiyemba',
        'role': 'user',
        'created_at': '2024-04-15',
    },
]


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash"""
    return hash_password(password) == hashed


def find_user_by_email(email: str) -> Optional[Dict]:
    """Find a user by email (case-insensitive)"""
    email_lower = email.lower().strip()
    for user in SAMPLE_USERS:
        if user['email'].lower() == email_lower:
            return user
    return None


def extract_surname(name: str) -> str:
    """Extract surname (last name) from full name"""
    if not name:
        return ''
    parts = name.strip().split()
    return parts[-1] if len(parts) > 1 else parts[0] if parts else ''


def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate a user and return user data if successful"""
    user = find_user_by_email(email)
    if not user:
        return None
    
    if verify_password(password, user['password']):
        # Return user data without password
        user_data = {k: v for k, v in user.items() if k != 'password'}
        # Extract surname from name
        user_data['surname'] = extract_surname(user_data.get('name', ''))
        return user_data
    
    return None


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_all_users() -> List[Dict]:
    """Get all users (without passwords)"""
    return [{k: v for k, v in user.items() if k != 'password'} for user in SAMPLE_USERS]


# Save users to JSON file for reference
def save_users_to_file():
    """Save user list to JSON file (without passwords)"""
    users_data = get_all_users()
    # Get backend directory (where this file is located)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(backend_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    users_file = os.path.join(data_dir, 'users.json')
    with open(users_file, 'w') as f:
        json.dump(users_data, f, indent=2)
    print(f"✅ Saved {len(users_data)} users to {users_file}")


if __name__ == '__main__':
    # Save users when run directly
    save_users_to_file()
    print("\nSample Users Created:")
    print("=" * 60)
    print("Admin Account:")
    print("  Email: admin@business.com")
    print("  Password: admin123")
    print("\nUser Accounts (7 users):")
    for i, user in enumerate(SAMPLE_USERS[1:], 1):
        print(f"  User {i}: {user['email']} / user123")


    # Save users when run directly
    save_users_to_file()
    print("\nSample Users Created:")
    print("=" * 60)
    print("Admin Account:")
    print("  Email: admin@business.com")
    print("  Password: admin123")
    print("\nUser Accounts (7 users):")
    for i, user in enumerate(SAMPLE_USERS[1:], 1):
        print(f"  User {i}: {user['email']} / user123")

