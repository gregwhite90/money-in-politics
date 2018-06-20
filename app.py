from flask import Flask, render_template
import tasks

app = Flask(__name__)

@app.route('/')
def homepage():
    cycle = '2016'
    office = 'president'

    fec_api_query = {
        'sort': '-total_receipts',
        'office': office,
        'election_full': 'true',
        'cycle': cycle,
    }
    
    query_response = tasks.fec_request('elections/', fec_api_query).text
    return render_template('index.html',
                           query=' '.join([cycle, office]),
                           query_response=query_response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
