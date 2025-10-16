#!/usr/bin/env python3
"""
Authentication Manager for Ping CRM
Handles password hashing and API key encryption
"""

import bcrypt
from cryptography.fernet import Fernet
import os
from typing import Tuple, Optional
from .db_manager import DatabaseManager


class AuthManager:
    """Manages user authentication and API key encryption"""

    def __init__(self, encryption_key: str = None):
        """
        Initialize auth manager

        Args:
            encryption_key: Base64-encoded Fernet key for encrypting API keys
                          If not provided, will look for ENCRYPTION_KEY env var
        """
        self.db = DatabaseManager()

        # Get or generate encryption key
        if encryption_key is None:
            encryption_key = os.getenv('ENCRYPTION_KEY')

        if encryption_key is None:
            raise ValueError(
                "ENCRYPTION_KEY not found in environment. "
                "Generate one with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
            )

        self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)

    @staticmethod
    def generate_encryption_key() -> str:
        """Generate a new Fernet encryption key"""
        return Fernet.generate_key().decode()

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)  # 12 rounds = good security/speed balance
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception:
            return False

    def encrypt_key(self, api_key: str) -> str:
        """Encrypt an API key"""
        if not api_key:
            return ''
        encrypted = self.cipher.encrypt(api_key.encode('utf-8'))
        return encrypted.decode('utf-8')

    def decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt an API key"""
        if not encrypted_key:
            return ''
        try:
            decrypted = self.cipher.decrypt(encrypted_key.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return ''

    def register_user(self, email: str, password: str,
                     apollo_key: str, notion_token: str,
                     notion_db_id: str, ai_key: str = None,
                     ai_provider: str = 'openai') -> Tuple[bool, str]:
        """
        Register a new user

        Returns:
            (success, message)
        """
        # Validate inputs
        if not email or '@' not in email:
            return False, "Invalid email address"

        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if not apollo_key or not notion_token or not notion_db_id:
            return False, "All API keys are required"

        # Check if user exists
        if self.db.user_exists(email):
            return False, "Email already registered"

        # Hash password
        password_hash = self.hash_password(password)

        # Encrypt API keys
        encrypted_apollo = self.encrypt_key(apollo_key)
        encrypted_notion_token = self.encrypt_key(notion_token)
        encrypted_notion_db = self.encrypt_key(notion_db_id)
        encrypted_ai = self.encrypt_key(ai_key) if ai_key else None

        # Create user
        success = self.db.create_user(
            email=email,
            password_hash=password_hash,
            encrypted_apollo=encrypted_apollo,
            encrypted_notion_token=encrypted_notion_token,
            encrypted_notion_db=encrypted_notion_db,
            encrypted_ai=encrypted_ai,
            ai_provider=ai_provider
        )

        if success:
            return True, "Registration successful!"
        else:
            return False, "Failed to create user account"

    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Authenticate user and return decrypted API keys

        Returns:
            (success, message, user_data_with_keys)
        """
        # Get user from database
        user = self.db.get_user_by_email(email)

        if not user:
            return False, "Invalid email or password", None

        # Verify password
        if not self.verify_password(password, user['password_hash']):
            return False, "Invalid email or password", None

        # Decrypt API keys
        decrypted_data = {
            'email': user['email'],
            'apollo_key': self.decrypt_key(user['encrypted_apollo_key']),
            'notion_token': self.decrypt_key(user['encrypted_notion_token']),
            'notion_db_id': self.decrypt_key(user['encrypted_notion_db_id']),
            'ai_key': self.decrypt_key(user['encrypted_ai_key']) if user['encrypted_ai_key'] else None,
            'ai_provider': user['ai_provider'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }

        # Update last login
        self.db.update_last_login(email)

        return True, "Login successful!", decrypted_data

    def update_user_password(self, email: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Update user password"""
        # Verify old password first
        user = self.db.get_user_by_email(email)
        if not user:
            return False, "User not found"

        if not self.verify_password(old_password, user['password_hash']):
            return False, "Current password is incorrect"

        if len(new_password) < 8:
            return False, "New password must be at least 8 characters"

        # Hash new password
        new_hash = self.hash_password(new_password)

        # Update in database
        # Note: This would need a new method in db_manager
        # For now, return not implemented
        return False, "Password update not yet implemented"

    def validate_api_keys(self, apollo_key: str, notion_token: str,
                         notion_db_id: str, ai_key: str = None) -> Tuple[bool, str]:
        """
        Validate API keys before registration

        Returns:
            (valid, message)
        """
        try:
            # Import clients for validation
            from .apollo_client import ApolloClient
            from notion_client import Client

            # Test Apollo
            apollo = ApolloClient(apollo_key)
            test_company = apollo.search_company("Google")
            if not test_company:
                return False, "Apollo API key invalid"

            # Test Notion
            client = Client(auth=notion_token)
            try:
                client.databases.query(database_id=notion_db_id, page_size=1)
            except Exception as e:
                return False, f"Notion credentials invalid: {str(e)}"

            # Test AI key if provided
            if ai_key:
                if ai_key.startswith('sk-'):
                    # OpenAI
                    import openai
                    openai.api_key = ai_key
                    try:
                        openai.models.list()
                    except Exception as e:
                        return False, f"OpenAI API key invalid: {str(e)}"
                else:
                    # Gemini
                    import google.generativeai as genai
                    try:
                        genai.configure(api_key=ai_key)
                        genai.list_models()
                    except Exception as e:
                        return False, f"Gemini API key invalid: {str(e)}"

            return True, "All API keys validated successfully!"

        except Exception as e:
            return False, f"Validation error: {str(e)}"
