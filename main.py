from flask import Flask
from flask import render_template
from flask import request

import httplib
import json
import urllib
import random

from helper import get_api_results_from_url
from wikiquotes import get_quote

app = Flask(__name__)
app.config.from_object('config')

@app.route('/test')
def test():
  image_url = 'https://portalstoragewuprod.azureedge.net/vision/Analysis/5-1.jpg'
  url = app.config['URL']
  key = app.config['CV_KEY']
  result = get_api_results_from_url(image_url, ['ImageType'], url, key)
  print get_quote()
  return json.dumps(result)

@app.route('/')
def homepage():
  return 'Machine Visionary'

if __name__ == '__main__':
  # server is publicly available
  app.run(host='0.0.0.0', port=8000)
