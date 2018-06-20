from flask import Flask, render_template
import tasks

app = Flask(__name__)

@app.route('/')
def homepage():
    query = 'Cruz, Rafael'
    query_response = tasks.fec_request('candidates/search/', query).text
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
