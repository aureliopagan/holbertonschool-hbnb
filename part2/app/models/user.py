from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    def validate_name(self, name, field_name):
        """Validate first_name and last_name"""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError(f"{field_name} is required and cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return name.strip()

    def validate_email(self, email):
        """Validate email format"""
        if not email or not isinstance(email, str) or not email.strip():
            raise ValueError("Email is required and cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            raise ValueError("Email must be in a valid format")
        
        return email.strip()

    def update(self, data):
        """Override update to include validation"""
        if 'first_name' in data:
            data['first_name'] = self.validate_name(data['first_name'], "First name")
        if 'last_name' in data:
            data['last_name'] = self.validate_name(data['last_name'], "Last name")
        if 'email' in data:
            data['email'] = self.validate_email(data['email'])
        
        super().update(data)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
