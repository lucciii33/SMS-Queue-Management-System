"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from dataEs import Queue
from sms import send
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

queue = Queue()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/new', methods=['POST'])
def post_queue():
    guest = request.json
    size = queue.size()
    queue.enqueue(guest)
    response_body = {
        "msg": f"Hello,{guest['name']} you ve been added, there are {size} in front of you"
    }

    return jsonify(response_body), 200

@app.route('/next', methods=['GET'])
def get_queue():
    if queue.size():
        removed_guest = queue.dequeue()
        send(body=f"{removed_guest['name']}, your table is ready", to=removed_guest['number'])
        response_body = {

            "msg": f"{removed_guest['name']}, was contacted"
        }
    else:
        response_body = {
            "msg": f"no people in the queue"
        }
    return jsonify(response_body), 200

@app.route('/all', methods=['GET'])
def get_all():
    return jsonify(queue.get_queue()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
