from app.models.base_model import BaseModel
from app import bcrypt
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)

    def validate_name(self, name, field_name):
        """Validate name fields"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if not name.strip():
            raise ValueError(f"{field_name} cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return name.strip()

    def validate_email(self, email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email = email.strip()
        if not email:
            raise ValueError("Email cannot be empty")
        
        # Enhanced email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user to dictionary excluding password"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.id} - {self.first_name} {self.last_name}>"