from flask import Blueprint, jsonify
from flask_restful import Api, Resource  # used for REST API building

student_api = Blueprint('student_api', __name__, url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

class StudentAPI:
    @staticmethod
    def get_student(name):
        students = {
            "Hannah": {
                "first name": "Hannah",
                "last name": "Li",
                "username": "hannahli_11",
                "favorite artists": "Gracie Abrams, Don Toliver, Ariana Grande",
            },
            "Rhea": {
                "first name": "Rhea",
                "last name": "Rajeshakhar",
                "username": "rhear_02",
                "favorite artists": "The Weeknd, Don Toliver, Metro Boomin",
            },
            "Gaheera": {
                "first name": "Gaheera",
                "last name": "Babbar",
                "username": "gaheerb",
                "favorite artists": "Future, Don Toliver, Travis Scott",
            },
            "Carson": {
                "first name": "Carson",
                "last name": "Sutherland",
                "username": "carsonsuth17",
                "favorite artists": "Brent Faiyaz, Radiohead, Drake",
            },
            "Rowan": {
                "first name": "Rowan",
                "last name": "Sutherland",
                "username": "rowangs",
                "favorite artists": "Hozier,  Imogen Heap, Big Theif",
            },
             "Brandon": {
                "first name": "Brandon",
                "last name": "Smurlo",
                "username": "bsmurlo",
                "favorite artists": "T-dre, Bryson Tiller, Bob Marley",
            }
        }
        return students.get(name)
    
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
api.add_resource(HannahResource, '/student/hannah')
api.add_resource(RheaResource, '/student/rhea')
api.add_resource(GaheeraResource, '/student/gaheera')
api.add_resource(RowanResource, '/student/rowan')
api.add_resource(CarsonResource, '/student/carson')
api.add_resource(BrandonResource, '/student/brandon')
