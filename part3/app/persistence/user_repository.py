# app/persistence/user_repository.py
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)  # This sets self.model = User

    def get_user_by_email(self, email):
        # Use the same pattern as your base SQLAlchemyRepository
        return self.model.query.filter_by(email=email).first()

    def create_admin_user(self, first_name, last_name, email, password):
        existing = self.get_user_by_email(email)
        if existing:
            return existing
        
        admin_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=True
        )
        admin_user.hash_password(password)
        
        # Use the inherited add method from SQLAlchemyRepository
        self.add(admin_user)
        return admin_user