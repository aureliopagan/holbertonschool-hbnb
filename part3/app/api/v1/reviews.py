from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        current_user = get_jwt_identity()

        review_data = api.payload
        place = facade.get_place(review_data["place_id"])

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user["id"]:
            return {"error": "You cannot review your own place."}, 400
        
        reviews = facade.get_reviews_by_place(review_data["place_id"])
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
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404
        if review.user_id != current_user["id"] and not current_user.get('is_admin', False):
            return {"error": "Unauthorized action"}, 403

        updated_details = api.payload
        
        # Create a dictionary for updated attributes
        updated_data = {}
        
        if "text" in updated_details:
            updated_data["text"] = updated_details["text"]

        if "rating" in updated_details:
            if not isinstance(updated_details["rating"], int) or not (1 <= updated_details["rating"] <= 5):
                return {"error": "Rating must be an integer between 1 and 5"}, 400
            updated_data["rating"] = updated_details["rating"]

        facade.update_review(review_id, updated_data)
        return {"message": "Review updated successfully"}, 200


    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if review.user_id != current_user["id"] and not current_user.get('is_admin', False):
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