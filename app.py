from flask import Flask
import requests
import os
app = Flask(__name__)

def fec_request(endpoint, query):
    payload = {
        'api_key': os.environ['DATAGOV_API_KEY'],
        'q': query,
        'sort': 'name',
        'page': 1
    }
    base_uri = 'https://api.open.fec.gov/v1/'
    r = requests.get(base_uri + endpoint, params=payload)
    return r
    
@app.route('/')
def homepage():
    return fec_request('candidates/search/', 'Cruz, Rafael').text

if __name__ == '__main__':
    app.run(debug=True)
