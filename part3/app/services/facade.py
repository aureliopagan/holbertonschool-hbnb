from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository(User)
        self.place_repo = PlaceRepository(Place)
        self.review_repo = AmenityRepository(Review)
        self.amenity_repo = ReviewRepository(Amenity)


    """User methods"""
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user
    

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(new_data)
        return user


    """Amenity methods"""
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity
    

    """Place methods"""
    def create_place(self, place_data):
        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
            else:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
    
        # Ensure the Place object only has owner_id, not the full owner object
        place_data["amenities"] = amenities
        place = Place(**place_data)
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
        return place
    

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            self.place_repo.delete(place_id)
        return {"message": "Place deleted successfully"}


    """Reviews methods"""
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        place_rating = int(review_data.get('rating'))
        if not user_id or not place_id:
            raise ValueError("User ID and Place ID must be provided.")
        if 5 < place_rating < 1:
            raise ValueError("Rating must be between 1 and 5")
        place = self.get_place(place_id)
        
        review = Review(**review_data)
        if place:
            self.place_repo.add(review)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return place.reviews
        return []


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.update(review_id, review_data)
        return review_data


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}