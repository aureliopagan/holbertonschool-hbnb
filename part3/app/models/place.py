from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description  # Optional field
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        """Validate title"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title

    def validate_price(self, price):
        """Validate price"""
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
        
        if price_float <= 0:
            raise ValueError("Price must be a positive value")
        return price_float

    def validate_latitude(self, latitude):
        """Validate latitude"""
        try:
            lat_float = float(latitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a valid number")
        
        if not (-90.0 <= lat_float <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return lat_float

    def validate_longitude(self, longitude):
        """Validate longitude"""
        try:
            lon_float = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a valid number")
        
        if not (-180.0 <= lon_float <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return lon_float

    def validate_owner(self, owner):
        """Validate owner"""
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")
        return owner

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)

    def update(self, data):
        """Override update to include validation"""
        if 'title' in data:
            data['title'] = self.validate_title(data['title'])
        if 'price' in data:
            data['price'] = self.validate_price(data['price'])
        if 'latitude' in data:
            data['latitude'] = self.validate_latitude(data['latitude'])
        if 'longitude' in data:
            data['longitude'] = self.validate_longitude(data['longitude'])
        if 'owner' in data:
            data['owner'] = self.validate_owner(data['owner'])
        
        super().update(data)
