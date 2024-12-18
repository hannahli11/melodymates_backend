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
            "Gaheera": {
                "Name": "Gaheera",
                "Bio": "Hi! I'm from San Diego and I go to Del Norte High School.",
                "Top 5 Artists": "Ariana Grande, Don Toliver, Kendrik Lamar, Drake, The Weeknd",
            },