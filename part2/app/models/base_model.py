class BaseModel:
    def __init__(self):
        self.id = self.generate_id()
        self.created_at = self.get_current_time()
        self.updated_at = self.created_at

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())

    def get_current_time(self):
        from datetime import datetime
        return datetime.now()

    def save(self):
        self.updated_at = self.get_current_time()
        # Logic to save the instance to storage

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }