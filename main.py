from flask import Flask
from flask import render_template
from flask import request

import httplib
import json
import urllib
import random

from helper import get_api_results_from_url
from wikiquotes import get_quote
from parse_vision_text import ParseVisionText

app = Flask(__name__)
app.config.from_object('config')
parser = ParseVisionText()


def resize(width, height):
	resized_w = width
	resized_h = height
	while resized_w > 720 or resized_h > 720:
		resized_w *= 0.8
		resized_h *= 0.8

	return (resized_w, resized_h)


@app.route('/test')
def test():
  quote = get_quote()
  image_url = 'https://stephanieye.files.wordpress.com/2014/03/0080-pie-on-scooter.jpg'
  url = app.config['URL']
  key = app.config['CV_KEY']
  result = get_api_results_from_url(image_url, ['Description', 'Categories', 'Tags'], url, key)
  tags = result['description']['tags']
  title = result['tags'][0]['name']
  print title
  print tags
  print quote
  print parser.demotivate(quote['quote'], tags)

  width, height = resize(result['metadata']['width'], result['metadata']['height'])
	#return json.dumps({'tags':tags, 'title':title})
	#return json.dumps(result)
  return render_template('poster.html', image_url=image_url, img_h=height, img_w=width)

@app.route('/')
def homepage():
  return 'Machine Visionary'

if __name__ == '__main__':
  # server is publicly available
  app.run(host='0.0.0.0', port=8000)
