
import json
import time
import os
from datetime import datetime
import random

from flask import Flask, make_response, request, jsonify, Response, send_file, render_template
from flask_cors import CORS, cross_origin
from threading import Thread
import hashlib
from DatabaseManagement import DatabaseManagement

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

database = None


def configure():
    global database
    with open('configuration.json') as configurationFile:
        configuration = json.load(configurationFile)
        database_configuration = configuration['DatabaseConfiguration']

    database = DatabaseManagement(database_configuration['connection_string'])


@app.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(database.get_user(details=False, username=None)), 200)


@app.route('/users/details', methods=['GET'])
def get_users_details():
    return make_response(jsonify(database.get_user(details=True, username=None)), 200)


@app.route('/user/create', methods=['POST'])
def create_user():
    user_create_response = database.create_user(request.json)
    if user_create_response[1]:
        return make_response(jsonify(user_create_response[0]), 200)
    return make_response(jsonify(user_create_response[0]), 400)


@app.route('/user/<username>', methods=['GET', 'DELETE', 'PUT'])
def manage_user(username):
    if request.method == "GET":
        return make_response(jsonify(database.get_user(details=False, username=username)), 200)
    elif request.method == "DELETE":
        return make_response(jsonify(database.delete_user(username)), 200)
    elif request.method == "PUT":
        print(request.json)
        return make_response(jsonify(database.update_user(username, request.json)), 200)
    else:
        return make_response("Bad request", 400)


if __name__ == '__main__':
    configure()
    app.run()
