# from flask import Flask, request, jsonify, Blueprint
# from flask_restful import Api, Resource
# from flask_cors import CORS
# # from model.musicpref import User, db, init_users  # Import your model

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, supports_credentials=True, origins='*')

# # Configure database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_management.db'  # Uses user_management.db
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# # Register Blueprint
# usermatching_api = Blueprint('usermatching_api', __name__, url_prefix='/api')
# api = Api(usermatching_api)

# # Initialize database
# with app.app_context():
#     db.create_all()
#     init_users()

# # ✅ Get all users from the database
# class AllUsersResource(Resource):
#     def get(self):
#         return jsonify(User.get_all_users())

# # ✅ Get a single user by name
# class UserResource(Resource):
#     def get(self, username):
#         user = User.get_user_by_name(username)
#         if user:
#             return jsonify(user.read())
#         return {"message": "User not found"}, 404

# # ✅ Edit a user's music preferences
# class EditUserPreferences(Resource):
#     def put(self, username):
#         user = User.get_user_by_name(username)
#         if not user:
#             return {"message": "User not found"}, 404
        
#         data = request.get_json()
#         if not data:
#             return {"message": "No data provided"}, 400
        
#         # Update preferences only if the song exists in the original data structure
#         valid_songs = [
#             "Black Star - Radiohead", "Sicko Mode - Travis Scott",
#             "Bad Guy - Billie Eilish", "No Tears Left to Cry - Ariana Grande",
#             "Ex-Factor - Lauryn Hill"
#         ]
#         for song, response in data.items():
#             if song in valid_songs and response in ["Yes", "No"]:
#                 user.preferences[song] = response

#         db.session.commit()
#         return jsonify(user.read())

# # ✅ Delete a user
# class DeleteUserResource(Resource):
#     def delete(self, username):
#         user = User.get_user_by_name(username)
#         if not user:
#             return {"message": "User not found"}, 404

#         db.session.delete(user)
#         db.session.commit()
#         return {"message": f"User '{username}' deleted successfully"}

# # Add API routes
# api.add_resource(AllUsersResource, '/users')  # Get all users
# api.add_resource(UserResource, '/match/<string:username>')  # Get single user
# api.add_resource(EditUserPreferences, '/match/<string:username>')  # Edit preferences
# api.add_resource(DeleteUserResource, '/match/<string:username>')  # Delete user

# # Register API Blueprint
# app.register_blueprint(usermatching_api)

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)
