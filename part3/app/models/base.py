import uuid
from datetime import datetime, timezone
from app import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    def save(self):
        self.updated_at = datetime.now(timezone.utc)


    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()