from flask import Flask, jsonify, Blueprint
from flask_restful import Api

userdata_api = Blueprint('userdata_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(userdata_api)

app = Flask(__name__)

