from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('reviews', description='Reviews operations')
# Define the models for related entities
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        # FIX: Use the new JWT format
        current_user_id = get_jwt_identity()    # This is now a string (user ID)
        claims = get_jwt()                      # This gets the additional claims
        is_admin = claims.get('is_admin', False)

        review_data = api.payload
        place = facade.get_place(review_data["place_id"])

        if not place:
            return {"error": "Place not found"}, 404

        # FIX: Compare string to string
        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place."}, 400
        
        reviews = facade.get_reviews_by_place(review_data["place_id"])
        for review in reviews:
            # FIX: Compare string to string
            if review.user_id == current_user_id:
                return {"error": "You have already reviewed this place."}, 400

        new_review = facade.create_review(review_data)
        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 201
    
    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.review_repo.get_all()
        if not reviews:
            return {"error": "No reviews found"}, 404
        return [
            {
            "id": review.id,
            "text": review.text,
            "rating": review.rating
            } for review in reviews
        ], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200


    @api.expect(review_model)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def put(self, review_id):
        """Update review's data"""
        # FIX: Use the new JWT format
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404
            
        # FIX: Compare string to string
        if review.user_id != current_user_id and not is_admin:
            return {"error": "Unauthorized action"}, 403

        # ... rest of method

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # FIX: Use the new JWT format
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
            
        # FIX: Compare string to string
        if review.user_id != current_user_id and not is_admin:
            return {"error": "Unauthorized action"}, 403
            
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}


@api.route("/places/<place_id>/reviews")
@api.doc(params={'place_id': 'ID of the place'})
class PlaceReviewsList(Resource):
    @api.expect(review_model)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self, place_id):
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data["place_id"] = place_id
        review_data["user_id"] = current_user["id"]

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user["id"]:
            return {"error": "You cannot review your own place."}, 400

        reviews = facade.get_reviews_by_place(place_id)
        for review in reviews:
            if review.user_id == current_user["id"]:
                return {"error": "You have already reviewed this place."}, 400

        new_review = facade.create_review(review_data)
        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 201
    
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        print(reviews)
        if not reviews:
            return {"error": "No reviews found for this place"}, 404
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
            } for review in reviews
        ], 200