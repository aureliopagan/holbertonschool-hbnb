#!/usr/bin/env python3
"""
Database initialization script
Run this to create all tables and add initial data
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables (careful - this deletes all data!)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Tables created successfully!")
        
        # Add initial data
        print("Adding initial data...")
        
        # Create admin user
        admin_user = User(
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            is_admin=True
        )
        admin_user.hash_password("admin123")  # You should use a secure password
        
        # Create a regular user for testing
        test_user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            is_admin=False
        )
        test_user.hash_password("password123")
        
        db.session.add(admin_user)
        db.session.add(test_user)
        db.session.commit()
        
        # Create amenities
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Swimming Pool")
        ac = Amenity(name="Air Conditioning")
        parking = Amenity(name="Parking")
        kitchen = Amenity(name="Kitchen")
        
        db.session.add_all([wifi, pool, ac, parking, kitchen])
        db.session.commit()
        
        # Create sample places
        place1 = Place(
            title="Cozy Beach House",
            description="Beautiful house near the beach with amazing ocean views",
            price=150.0,
            latitude=25.7617,
            longitude=-80.1918,
            owner_id=admin_user.id
        )
        place1.amenities = [wifi, pool, kitchen]
        
        place2 = Place(
            title="Mountain Cabin",
            description="Peaceful cabin in the mountains, perfect for relaxation",
            price=100.0,
            latitude=39.7392,
            longitude=-104.9903,
            owner_id=test_user.id
        )
        place2.amenities = [wifi, ac, parking]
        
        place3 = Place(
            title="City Apartment",
            description="Modern apartment in the heart of the city",
            price=200.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=admin_user.id
        )
        place3.amenities = [wifi, ac, kitchen]
        
        place4 = Place(
            title="Lakeside Cottage",
            description="Charming cottage by the lake with fishing access",
            price=75.0,
            latitude=44.9778,
            longitude=-93.2650,
            owner_id=test_user.id
        )
        place4.amenities = [wifi, parking]
        
        db.session.add_all([place1, place2, place3, place4])
        db.session.commit()
        
        # Need to get the IDs after commit
        db.session.flush()  # This assigns IDs without committing
        
        # Create sample reviews
        review1 = Review(
            text="Amazing place! The view was incredible and the host was very friendly.",
            rating=5,
            user_id=test_user.id,
            place_id=place1.id
        )
        
        review2 = Review(
            text="Great location and very clean. Would definitely stay again!",
            rating=4,
            user_id=admin_user.id,
            place_id=place2.id
        )
        
        review3 = Review(
            text="Perfect for a city getaway. Close to everything we needed.",
            rating=5,
            user_id=test_user.id,
            place_id=place3.id
        )
        
        db.session.add_all([review1, review2, review3])
        db.session.commit()
        
        print("Initial data added successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Amenity.query.count()} amenities")
        print(f"Created {Place.query.count()} places")
        print(f"Created {Review.query.count()} reviews")
        print("\nDatabase initialization complete!")
        print("\nTest users created:")
        print("  Admin: admin@hbnb.io / admin123")
        print("  User: john@example.com / password123")

if __name__ == "__main__":
    init_database()