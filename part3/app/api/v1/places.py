from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('places', description='Place operations')
# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner'),
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(api.model('Owner', {
        'id': fields.String(description='User ID of the owner'),
        'first_name': fields.String(description='First name of the owner'),
        'last_name': fields.String(description='Last name of the owner'),
        'email': fields.String(description='Email of the owner')
    })),
    'amenities': fields.List(fields.String, description="List of amenity IDs"),
})


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()  # This is now a string (user ID)
        claims = get_jwt()  # This gets the additional claims
        is_admin = claims.get('is_admin', False)
        
        place_data = api.payload
        place_data['owner_id'] = current_user_id  # Set the owner_id
        
        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': current_user_id,
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in new_place.amenities
            ]
        }, 201


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.place_repo.get_all()
        if not places:
            return {"error": "No places found"}, 404
        return [
            {
                'id': place.id,
                'title': place.title,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
            }
            for place in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'reviews': [
                {
                    'text': review.text,
                    'rating': review.rating
                } for review in place.reviews
            ],
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in place.amenities
            ]
        }, 200


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if not current_user:
            return {"error": "Unauthorized"}, 401

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id != current_user.id and not current_user.is_admin:
            return {"error": "Unauthorized action"}, 403

        updated_details = api.payload or {}

        # Handle amenities
        updated_amenities = []
        for amenity_id in updated_details.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                updated_amenities.append(amenity)
        updated_details['amenities'] = updated_amenities

        # If updating owner_id (not common), validate that new owner exists
        if 'owner_id' in updated_details:
            new_owner = facade.get_user(updated_details['owner_id'])
            if not new_owner:
                return {"error": "Owner not found"}, 404
            updated_details['owner_id'] = new_owner.id

        facade.update_place(place_id, updated_details)
        return {"message": "Place updated successfully"}, 200