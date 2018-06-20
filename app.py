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
    
    query_response = tasks.fec_request('elections/', fec_api_query)

    # to add error checking
    
    chart_params = {
        'type': 'bar',
        'labels': [],
        'values': []
    }

    min_receipts = 5000000.0

    for result in query_response.json()['results']:
        if result['total_receipts'] < min_receipts: break
        chart_params['labels'].append(result['candidate_name'])
        chart_params['values'].append(result['total_receipts'])
        
    
    return render_template('index.html',
                           query=' '.join([cycle, office]),
                           chart_params=chart_params)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
