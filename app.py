import flask
from flask import request, jsonify, abort
from flask_cors import CORS, cross_origin
import json
import git

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Create some test data for our catalog in the form of a list of dictionaries.

with open ('tasks.json', 'r') as f:
    tasks = json.load(f)



@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return '''<h1>Simple api for tasks app</h1>
<p>Please don't hack this.</p>
<p>Made by <a href="https://www.zoesobol.com.ar">Zoe Sobol</a></p>'''


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/zoesobol/fast-tracker-api.git')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

# A route to return all of the available entries in our catalog.
@app.route('/tasks/', methods=['POST'])
@cross_origin()
def api_post():
    text = request.json['text']
    day = request.json['day']
    reminder = request.json['reminder']
    task = {
        'id': len(tasks['tasks'])+1,
        'text': text,
        'day': day,
        'reminder': reminder
    }
    tasks['tasks'].append(task)
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@cross_origin()
def api_delete(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    tasks.remove(task[0])
    return jsonify(tasks)

@app.route('/tasks/', methods=['GET'])
@cross_origin()
def api_all():
    return jsonify(tasks['tasks'])

@app.route('/tasks/<int:task_id>', methods=['GET'])
@cross_origin()
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for task in tasks:
        if task['id'] == id:
            results.append(task)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
