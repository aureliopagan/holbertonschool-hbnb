from app.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app import db


place_amenity = db.Table('place_amenity',
                         Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
                         Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
                         )


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship(
        'Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))