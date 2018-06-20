from flask import Flask, render_template

app = Flask(__name__)

from rq import Queue
from worker import conn
import utils

q = Queue(connection=conn)

@app.route('/')
def homepage():
    query = 'Cruz, Rafael'
    query_response = q.enqueue(utils.fec_request, 'candidates/search/', query).text
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
