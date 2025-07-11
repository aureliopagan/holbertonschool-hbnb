from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    def validate_text(self, text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        return text

    def validate_rating(self, rating):
        """Validate rating"""
        try:
            rating_int = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be a valid integer")
        
        if not (1 <= rating_int <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating_int

    def validate_place(self, place):
        """Validate place"""
        # Import here to avoid circular imports
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")
        return place

    def validate_user(self, user):
        """Validate user"""
        from app.models.user import User
        if not isinstance(user, User):
            raise ValueError("User must be a User instance")
        return user

    def update(self, data):
        """Override update to include validation"""
        if 'text' in data:
            data['text'] = self.validate_text(data['text'])
        if 'rating' in data:
            data['rating'] = self.validate_rating(data['rating'])
        if 'place' in data:
            data['place'] = self.validate_place(data['place'])
        if 'user' in data:
            data['user'] = self.validate_user(data['user'])
        
        super().update(data)
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
