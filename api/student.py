from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS 

student_api = Blueprint('student_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)


class StudentAPI:
   # @app.route('/api/student/')
    # @app.route('/api/student/name')main
    def get_student(name):
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
                "FavoriteArtists": "Hozier,  Imogen Heap, Big Theif",
            },
             "Brandon": {
                "Firstname": "Brandon",
                "Lastname": "Smurlo",
                "Username": "bsmurlo",
                "Password": "yL!3vG7#qN2x@P5m",
                "FavoriteArtists": "T-dre, Bryson Tiller, Bob Marley",
            }
        }
        return students[name]
    
class HannahResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Hannah")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
    
class RheaResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Rhea")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
    
class RowanResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Rowan")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
    
class GaheeraResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Gaheera")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
    
class BrandonResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Brandon")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
    
class CarsonResource(Resource): 
    def get(self):
        student = StudentAPI.get_student("Carson")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404
        
# Building REST API endpoint
api.add_resource(HannahResource, '/student/Hannah')
api.add_resource(RheaResource, '/student/Rhea')
api.add_resource(GaheeraResource, '/student/Gaheera')
api.add_resource(RowanResource, '/student/Rowan')
api.add_resource(CarsonResource, '/student/Carson')
api.add_resource(BrandonResource, '/student/Brandon')
