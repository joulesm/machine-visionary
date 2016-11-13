import time 
import requests
import operator
import numpy as np

from flask import app

def process_request( url, json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:

            print "Message: ", response.json()

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print 'Error: failed after retrying!'
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print "Error code: ", response.status_code
            print "Message: ", response.json()

        break
        
    return result

def get_api_results_from_url(url_image, visual_features, url, key):
    feature_string = ",".join(visual_features)
    #Computer Vision Parameters
    params = { 'visualFeatures' : feature_string} 

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = key
    headers['Content-Type'] = 'application/json' 
    json = { 'url': url_image } 
    data = None

    result = process_request( url, json, data, headers, params )
    return result
