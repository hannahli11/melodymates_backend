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
    },
    "Rhea": {
        "Firstname": "Rhea",
        "Lastname": "Rajeshakhar",
        "Username": "rhear_02",
        "Password": "yM#7hX2%fJ5k!C9a",
        "FavoriteArtists": "The Weeknd, Don Toliver, Metro Boomin",
    },
    "Gaheera": {
        "Firstname": "Gaheera",
        "Lastname": "Babbar",
        "Username": "gaheerb",
        "Password": "tG@9pR1*Lz5x$Q3m",
        "FavoriteArtists": "Future, Don Toliver, Travis Scott",
    },
    "Carson": {
        "Firstname": "Carson",
        "Lastname": "Sutherland",
        "Username": "carsonsuth17",
        "Password": "vH!6yP3#nZ2q@X5f",
        "FavoriteArtists": "Brent Faiyaz, Radiohead, Drake",
    },
    "Rowan": {
        "Firstname": "Rowan",
        "Lastname": "Sutherland",
        "Username": "rowangs",
        "Password": "mA$2hN1@tX7p#Q9k",
        "FavoriteArtists": "Hozier, Imogen Heap, Big Thief",
    },
    "Brandon": {
        "Firstname": "Brandon",
        "Lastname": "Smurlo",
        "Username": "bsmurlo",
        "Password": "yL!3vG7#qN2x@P5m",
        "FavoriteArtists": "T-dre, Bryson Tiller, Bob Marley",
    },
}

# Define StudentAPI class
class StudentAPI:
    @staticmethod
    def get_student(name):
        return students.get(name, None)

    @staticmethod
    def put_student(firstname, lastname, username, password, favorite_artists):
        temp_student = {
            firstname: {
                "Firstname": firstname,
                "Lastname": lastname,
                "Username": username,
                "Password": password,
                "FavoriteArtists": favorite_artists,
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

    def post(self):
        data = request.get_json()
        required_fields = ["Firstname", "Lastname", "Username", "Password", "FavoriteArtists"]
        if all(field in data for field in required_fields):
            new_student = StudentAPI.put_student(
                data["Firstname"],
                data["Lastname"],
                data["Username"],
                data["Password"],
                data["FavoriteArtists"],
            )
            return jsonify(new_student)
        return {"error": "Missing fields in request"}, 400


# Add resources to the API
api.add_resource(StudentResource, '/student/<string:name>')  # GET specific student
api.add_resource(StudentResource, '/student')  # POST new student

# Register Blueprint with Flask app
app.register_blueprint(student_api)

if __name__ == "__main__":
    app.run(debug=True)
