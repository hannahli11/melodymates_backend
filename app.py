
from flask import Flask, jsonify
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/hannah')
def get_hannah_data():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Hannah",
        "LastName": "Li",
        "Username": "Hannahli_11"
    })
 # Return the list as JSON response
    return jsonify(InfoDb)

# add an api endpoint to flask app
@app.route('/api/carson')
def get_carson_data():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Carson",
        "LastName": "Sutherland",
        "Username": "CJSuth$"
    })
    return jsonify(InfoDb)

@app.route('/api/rhea')
def get_rhea_data():
    # start a list, to be used like a information database
    InfoDb = []
    InfoDb.append({
        "FirstName": "rhea",
        "LastName": "rajashekhar",
        "Username": "rhear$"
    })
    return jsonify(InfoDb)
    
# add an api endpoint to flask app
@app.route('/api/Brandon')
def get_brandon_data():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Brandon",
        "LastName": "Smurlo",
        "Username": "bsmurlo"
    })
    return jsonify(InfoDb)

@app.route('/api/rowan')
def get_brandon_data():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Rowan",
        "LastName": "Sutherland",
        "Username": "rowangs.1"
    })
    return jsonify(InfoDb)
# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)
