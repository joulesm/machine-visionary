from flask import Flask
from flask import render_template
from flask import request

import httplib
import urllib
import random


app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Machine Visionary'

if __name__ == '__main__':
    # auto reloads the server on changes, also enables debugging
    app.debug = True
    # server is publicly available
    app.run(host='0.0.0.0', port=8000)