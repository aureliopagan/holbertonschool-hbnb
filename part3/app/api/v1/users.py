from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route("/")
class UserList(Resource):


    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """Retrieve all users (admin only)"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user or not current_user.is_admin:
            return {"error": "Admin privileges required"}, 403

        users = facade.user_repo.get_all()
        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            } for user in users
        ], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {"error": "Email already registered"}, 400
        
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except (ValueError, TypeError, AssertionError) as e:
            return {"error": str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
        
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200
        except (ValueError, TypeError, AssertionError) as e:
            return {"error": str(e)}, 400
    

    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        # FIX: Use the new JWT format
        current_user_id = get_jwt_identity()    # This is now a string (user ID)
        claims = get_jwt()                      # This gets the additional claims
        is_admin = claims.get('is_admin', False)
        
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        # FIX: Compare string to string
        if user.id != current_user_id and not is_admin:
            return {"error": "Unauthorized action."}, 403
        
        updated_details = api.payload
        updated_user = facade.update_user(user_id, updated_details)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
    

@api.route('/public/')
class PublicUserList(Resource):
    def get(self):
        """Get all non-admin users (public endpoint)"""
        # Use the existing facade instead of creating a new repository
        users = facade.user_repo.get_all()
        non_admins = [user for user in users if not user.is_admin]
        return [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        } for user in non_admins], 200
