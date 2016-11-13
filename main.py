from flask import Flask
from flask import render_template
from flask import request
from wtforms import Form, TextField, validators

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


class ImageForm(Form):
    img_url = TextField('Image URL:', validators=[validators.required()])

def resize(width, height):
    resized_w = width
    resized_h = height
    while resized_w > IMAGE_MAX_W or resized_h > IMAGE_MAX_H:
        resized_w *= 0.8
        resized_h *= 0.8

    return (resized_w, resized_h)

def calculate_padding(max_size, size):
    return (max_size - size) / 2

def capitalize_sentence(sentence):
    words = sentence.split(' ')
    words[0] = words[0].title()
    return ' '.join(words)



@app.route('/demotivate', methods=['POST'])
def test():
    quote = get_quote()
    form = ImageForm(request.form)
    image_url = request.form['img_url']
    url = app.config['URL']
    key = app.config['CV_KEY']
    result = get_api_results_from_url(image_url, ['Description', 'Categories', 'Tags'], url, key)
    tags = result['description']['tags']
    print "TAGS: ", tags

    title = result['tags'][0]['name']
    # Find a title that's a little more interesting
    i = 0
    while title in ['outdoor', 'indoor', 'person']:
        i += 1
        try:
            title = result['tags'][i]['name']
        except IndexError:
            pass

    # Resize the image to fit the poster
    width, height = resize(result['metadata']['width'], result['metadata']['height'])
    # Calculate the necessary black padding to fill out the poster
    pad_w = calculate_padding(POSTER_W, width)
    pad_h = calculate_padding(POSTER_H, height)

    # Get the demotivated quote and also capitalize the first letter of the sentence
    demotivated_quote = capitalize_sentence(parser.demotivate(quote['quote'], tags))

    return render_template(
        'poster.html', image_url=image_url, img_h=height,
        img_w=width, pad_w=pad_w, pad_h=pad_h, title=title.upper(), quote=demotivated_quote,
        orig_quote=quote['quote'], tags=tags, author=quote['author'])

@app.route('/')
def homepage():
    return render_template('index.html', form=ImageForm(request.form))

if __name__ == '__main__':
    # server is publicly available
    app.run(host='0.0.0.0', port=8000)
