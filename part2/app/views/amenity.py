from flask import Blueprint, request, jsonify
from app.models.amenity import Amenity

amenity_bp = Blueprint('amenity', __name__)

@amenity_bp.route('/amenities', methods=['GET'])
def get_amenities():
    # Logic to retrieve all amenities
    amenities = []  # Replace with actual retrieval logic
    return jsonify(amenities), 200

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    # Logic to retrieve a specific amenity by ID
    amenity = None  # Replace with actual retrieval logic
    if amenity:
        return jsonify(amenity), 200
    return jsonify({'error': 'Amenity not found'}), 404

@amenity_bp.route('/amenities', methods=['POST'])
def create_amenity():
    # Logic to create a new amenity
    data = request.get_json()
    new_amenity = Amenity(**data)  # Replace with actual creation logic
    return jsonify(new_amenity), 201

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    # Logic to update an existing amenity
    data = request.get_json()
    updated_amenity = None  # Replace with actual update logic
    if updated_amenity:
        return jsonify(updated_amenity), 200
    return jsonify({'error': 'Amenity not found'}), 404

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    # Logic to delete an amenity
    success = False  # Replace with actual deletion logic
    if success:
        return jsonify({'message': 'Amenity deleted'}), 204
    return jsonify({'error': 'Amenity not found'}), 404