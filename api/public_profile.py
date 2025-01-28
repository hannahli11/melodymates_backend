from sqlite3 import IntegrityError
from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS 
import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.publicProfileData import PublicProfile


profile_api = Blueprint('profile_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(profile_api)

class ProfileAPI:
      
    class _CRUD(Resource):
        """
        API for Create, Read, Update, Delete operations on the PublicProfile model.
        """

        def post(self):
            """
            Create a new public profile.
            """
            body = request.get_json()

            # Validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': 'Name is missing or is less than 2 characters'}, 400

            # Validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': 'User ID is missing or is less than 2 characters'}, 400

            # Setup PublicProfile object
            profile_obj = PublicProfile(
                name=name,
                uid=uid,
                pfp=body.get('pfp', ''),
                bio=body.get('bio', ''),
                favorite_artist=body.get('favorite_artist', '')
            )

            profile = profile_obj.create(body)  # pass the body elements to be saved in the database
            if not profile:  # failure returns error message
                return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self):
            """
            Return the current user's profile as a JSON object.
            """
            # print("lol")
            # profile = g.current_user
            # profile_data = profile.read()
            # print(profile_data)
            # if not profile:
            #     return {'message': 'No profile found'}, 404
            
            # print("KJLASDFLKAJSDHFLKAJSDHFLKAJSDHFKLJASDHFLKAJSHDFLKJAHSDF")
            
            # return jsonify(profile_data)
            return "jamal"



        @token_required
        def put(self):
            """
            Update a public profile.
            """
            current_profile = g.current_user
            body = request.get_json()

            # Allow admins to update other profiles
            if current_profile and current_profile.uid == 'admin_user':  # Assuming 'admin_user' identifies admins
                uid = body.get('uid')
                if uid and uid != current_profile.uid:
                    profile = PublicProfile.query.filter_by(_uid=uid).first()
                    if not profile:
                        return {'message': f"Profile with UID {uid} not found"}, 404
                else:
                    profile = current_profile  # Admin is updating their own profile
            else:
                profile = current_profile  # Regular users can only update their own profile

            # Update profile fields
            profile.update(body)
            return jsonify(profile.__dict__)

        @token_required
        def delete(self):
            """
            Delete a public profile.
            """
            current_profile = g.current_user
            if not current_profile:
                return {'message': 'No profile found to delete'}, 404

            try:
                current_profile.delete()
                return {'message': f"Profile {current_profile.uid} deleted successfully"}, 200
            except Exception as e:
                return {'message': f"Error occurred: {str(e)}"}, 500

       
    class _Security(Resource):
        """
        Security-related API operations.
        """


        def post(self):
            """
            Authenticate a user and generate a JWT token.
            """
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400


                # Get Data
                uid = body.get('uid')
                if uid is None:
                    return {'message': 'User ID is missing'}, 401
                password = body.get('password')
                if not password:
                    return {'message': 'Password is missing'}, 401


                # Find user
                user = PublicProfile.query.filter_by(_uid=uid).first()


                # if user is None or not user.is_password(password):
                #     return {'message': "Invalid user id or password"}, 401


                # Generate token
                token = jwt.encode(
                    {"_uid": user._uid},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                resp = Response(f"Authentication for {user._uid} successful")
                resp.set_cookie(
                    current_app.config["JWT_TOKEN_NAME"],
                    token,
                    max_age=3600,
                    secure=True,
                    httponly=True,
                    path='/',
                    samesite='None'  # This is the key part for cross-site requests
                )
                return resp
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500


        @token_required()
        def delete(self):
            """
            Invalidate the current user's token by setting its expiry to 0.
            """
            current_user = g.current_user
            try:
                # Generate a token with practically 0 age
                token = jwt.encode(
                    {"_uid": current_user._uid, "exp": datetime.utcnow()},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )


                # Prepare a response indicating the token has been invalidated
                resp = Response("Token invalidated successfully")
                resp.set_cookie(
                    current_app.config["JWT_TOKEN_NAME"],
                    token,
                    max_age=0,  # Immediately expire the cookie
                    secure=True,
                    httponly=True,
                    path='/',
                    samesite='None'
                )
                return resp
            except Exception as e:
                return {
                    "message": "Failed to invalidate token",
                    "error": str(e)
                }, 500
    class _ID(Resource):  # Individual identification API operation
        @token_required()
        def get(self):
            ''' Retrieve the current user from the token_required authentication check '''
            current_user = g.current_user
            ''' Return the current user as a json object '''
            return jsonify(current_user.read())
        
# Building REST API endpoint
api.add_resource(ProfileAPI._ID, '/profileId')
api.add_resource(ProfileAPI._CRUD, '/profile')
api.add_resource(ProfileAPI._Security, '/profileAuthenticate')
