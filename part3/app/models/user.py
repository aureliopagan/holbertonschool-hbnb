from app.models.base import BaseModel
from app import db
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship('Place', backref='user', lazy=True)
    reviews = relationship('Review', backref='user', lazy=True)


    def hash_password(self, password):
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)