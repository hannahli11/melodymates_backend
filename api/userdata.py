from flask import Flask, jsonify, Blueprint
from flask_restful import Api

userdata_api = Blueprint('userdata_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(userdata_api)

app = Flask(__name__)

# Simulated database for user information
InfoDb = {
    "Hannah": {
        "FirstName": "Hannah",
        "LastName": "Li",
        "Username": "Hannahli_11"
    },
    "Carson": {
        "FirstName": "Carson",
        "LastName": "Sutherland",
        "Username": "CJSuth$"
    },
    "Rhea": {
        "FirstName": "Rhea",
        "LastName": "Rajashekhar",
        "Username": "rhear$"
    },
    "Brandon": {
        "FirstName": "Brandon",
        "LastName": "Smurlo",
        "Username": "bsmurlo"
    },
    "Rowan": {
        "FirstName": "Rowan",
        "LastName": "Sutherland",
        "Username": "rowangs.1"
    }
}

@app.route('/<string:user_name>')
def get_user_data(user_name):
    # Look up the user by name in the InfoDb
    user_data = InfoDb.get(user_name)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h2>Welcome to the User Data API</h2>
        <p>To access user data, append /[user_name] to the URL (e.g., /Hannah, /Carson, etc.).</p>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
