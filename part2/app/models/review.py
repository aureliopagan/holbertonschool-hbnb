from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = int(rating)
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")
        self.place = place
        self.user = user
