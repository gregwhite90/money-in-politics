from flask import Flask, render_template
import requests
import os
app = Flask(__name__)

def fec_request(endpoint, query):
    payload = {
        'api_key': os.environ.get('DATAGOV_API_KEY'), # to add default?
        'q': query,
        'sort': 'name',
        'page': 1
    }
    base_uri = 'https://api.open.fec.gov/v1/'
    r = requests.get(base_uri + endpoint, params=payload)
    return r
    
@app.route('/')
def homepage():
    query = 'Cruz, Rafael'
    query_response = fec_request('candidates/search/', query).text
    return render_template('index.html',
                           query=query,
                           query_response=query_response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
