from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource  # Used for REST API building
from flask_cors import CORS

# Initialize Flask app and Blueprint
student_api = Blueprint('student_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# API docs: https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

# Sample data
students = {
    "Hannah": {
        "Firstname": "Hannah",
        "Lastname": "Li",
        "Username": "hannahli_11",
        "Password": "rT$4vN8@qL3w!ZxP",
        "FavoriteArtists": "Gracie Abrams, Don Toliver, Ariana Grande",
        "Bio": "Music enthusiast and aspiring songwriter.",
        "ProfilePicture": "https://example.com/hannah_profile.jpg",
    },
    "Rhea": {
        "Firstname": "Rhea",
        "Lastname": "Rajeshakhar",
        "Username": "rhear_02",
        "Password": "yM#7hX2%fJ5k!C9a",
        "FavoriteArtists": "The Weeknd, Don Toliver, Metro Boomin",
        "Bio": "Future producer and music lover.",
        "ProfilePicture": "https://example.com/rhea_profile.jpg",
    },
}

# Define StudentAPI class
class StudentAPI:
    @staticmethod
    def get_student(name):
        return students.get(name, None)

    @staticmethod
    def put_student(firstname, lastname, username, password, favorite_artists, bio, profile_picture):
        temp_student = {
            firstname: {
                "Firstname": firstname,
                "Lastname": lastname,
                "Username": username,
                "Password": password,
                "FavoriteArtists": favorite_artists,
                "Bio": bio,
                "ProfilePicture": profile_picture,
            }
        }
        students[firstname] = temp_student[firstname]
        return temp_student[firstname]


# Define RESTful resources
class StudentResource(Resource):
    def get(self, name):
        student = StudentAPI.get_student(name)
        if student:
            return jsonify(student)
        return {"error": "Student not found"}, 404


class AddStudentResource(Resource):
    def post(self):
        # Extract data from request headers
        firstname = request.headers.get("Firstname")
        lastname = request.headers.get("Lastname")
        username = request.headers.get("Username")
        password = request.headers.get("Password")
        favorite_artists = request.headers.get("FavoriteArtists")
        bio = request.headers.get("Bio")
        profile_picture = request.headers.get("ProfilePicture")

        # Validate required fields
        if not all([firstname, lastname, username, password, favorite_artists, bio, profile_picture]):
            return {"error": "Missing required fields in headers"}, 400

        # Add new student to the dictionary
        students[firstname] = {
            "Firstname": firstname,
            "Lastname": lastname,
            "Username": username,
            "Password": password,
            "FavoriteArtists": favorite_artists,
            "Bio": bio,
            "ProfilePicture": profile_picture,
        }

        return students[firstname], 201  # Return the new student and HTTP 201 status


# Add resources to the API
api.add_resource(StudentResource, '/student/<string:name>', endpoint='get_student')  # GET specific student
api.add_resource(AddStudentResource, '/student', endpoint='add_student')  # POST new student

# Register Blueprint with Flask app
app.register_blueprint(student_api)

if __name__ == "__main__":
    app.run(debug=True)
