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

POSTER_W = 1024
POSTER_H = 640
IMAGE_MAX_W = 840
IMAGE_MAX_H = 525


def resize(width, height):
	resized_w = width
	resized_h = height
	while resized_w > IMAGE_MAX_W or resized_h > IMAGE_MAX_H:
		resized_w *= 0.8
		resized_h *= 0.8

	return (resized_w, resized_h)

def calculate_padding(max_size, size):
	return (max_size - size) / 2


@app.route('/test')
def test():
  quote = get_quote()
	image_url = 'https://stephanieye.files.wordpress.com/2014/03/0080-pie-on-scooter.jpg'
	url = app.config['URL']
	key = app.config['CV_KEY']
	result = get_api_results_from_url(image_url, ['Description', 'Categories', 'Tags'], url, key)
	tags = result['description']['tags']
	title = result['tags'][0]['name']
	width, height = resize(result['metadata']['width'], result['metadata']['height'])
	pad_w = calculate_padding(POSTER_W, width)
	pad_h = calculate_padding(POSTER_H, height)
  print parser.demotivate(quote['quote'], tags)
	#return json.dumps({'tags':tags, 'title':title})
	#return json.dumps(result)
	return render_template(
		'poster.html', image_url=image_url, img_h=height,
		img_w=width, pad_w=pad_w, pad_h=pad_h, title=title.upper(), quote="Make America great again!")

@app.route('/')
def homepage():
  return 'Machine Visionary'

if __name__ == '__main__':
  # server is publicly available
  app.run(host='0.0.0.0', port=8000)
