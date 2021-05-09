
import json
import time
import os
from datetime import datetime
import random

from flask import Flask, make_response, jsonify, Response, send_file, render_template
from flask_cors import CORS, cross_origin
from threading import Thread

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

database = None

def configure():
    print(3)

@app.route('/test')
def test():
    return make_response("OK", 200)


if __name__ == '__main__':
    app.run()

