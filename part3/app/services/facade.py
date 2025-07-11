from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            # Check if email is being updated and if it's unique
            if 'email' in user_data:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    raise ValueError("Email already registered")
            
            user.update(user_data)
            return user
        return None

    # Amenity methods
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
        return None

    # Place methods (placeholders for now)
    def create_place(self, place_data):
        pass

    def get_place(self, place_id):
        pass

    def get_all_places(self):
        pass

    def update_place(self, place_id, place_data):
        pass

    # Review methods (placeholders for now)
    def create_review(self, review_data):
        pass

    def get_review(self, review_id):
        pass

    def get_all_reviews(self):
        pass

    def update_review(self, review_id, review_data):
        pass

    def delete_review(self, review_id):
        pass

    def get_reviews_by_place(self, place_id):
        pass
