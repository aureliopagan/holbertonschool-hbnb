from app.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) #Change back to false
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)


    def get_place(self, id):
        from app.services import facade
        place = facade.get_place(id)
        return place
    

    def get_User(self, id):
        from app.services import facade
        user = facade.get_user(id)
        return user