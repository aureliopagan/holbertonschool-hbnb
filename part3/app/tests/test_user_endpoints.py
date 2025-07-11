import unittest
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    """ Test the API endpoints """

    def setUp(self):
        """ Set up the test client """
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    # Amenity Tests
    def test_create_amenity(self):
        """Test creating a new amenity"""
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_amenity_invalid_data(self):
        """Test creating amenity with invalid data"""
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test getting all amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity(self):
        """Test getting an amenity by its ID"""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        amenity_id = create_response.json['id']
        
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Wi-Fi")

    def test_get_amenity_not_found(self):
        """Test getting a nonexistent amenity"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # User Tests
    def test_create_user(self):
        """Test creating a new user"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_invalid_email(self):
        """Test creating user with invalid email"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)