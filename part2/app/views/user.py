from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.storage import Storage

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = Storage.get_all_users()  # Assuming a method to get all users
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Storage.get_user_by_id(user_id)  # Assuming a method to get user by ID
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(**data)  # Assuming User class can be initialized with data
    Storage.save_user(new_user)  # Assuming a method to save user
    return jsonify(new_user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = Storage.get_user_by_id(user_id)
    if user:
        user.update(**data)  # Assuming an update method in User class
        Storage.save_user(user)
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Storage.get_user_by_id(user_id)
    if user:
        Storage.delete_user(user_id)  # Assuming a method to delete user
        return jsonify({'message': 'User deleted'}), 204
    return jsonify({'error': 'User not found'}), 404