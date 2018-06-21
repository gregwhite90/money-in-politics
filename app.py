from flask import Flask, render_template, url_for
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
        'values': [],
        'candidate_links': []
    }

    min_receipts = 5000000.0

    for result in query_response.json()['results']:
        if result['total_receipts'] < min_receipts: break
        chart_params['labels'].append(result['candidate_name'])
        chart_params['values'].append(result['total_receipts'])
        chart_params['candidate_links'].append(
            url_for('candidate_summary',
                    candidate_fec_id=result['candidate_id']))
    
    return render_template('index.html',
                           query=' '.join([cycle, office]),
                           chart_params=chart_params)

@app.route('/candidate_summary/<candidate_fec_id>')
def candidate_summary(candidate_fec_id):
    cycle = '2016'
        
    fec_api_query = {
        'full_election': 'true',
        'cycle': cycle
    }
    
    query_response = tasks.fec_request('candidate/' +
                                       candidate_fec_id +
                                       '/totals/',
                                       fec_api_query)
    
    # to add error checking, incl length of results being 1

    result = query_response.json()['results'][0]

    chart_params = {
        'type': 'bar',
        'labels': [],
        'data': {
            'labels': [result['candidate_id']],
            'datasets': []
        },
        'options': {
            'scales': {
                'xAxes': [{
                    'stacked': True
                }],
                'yAxes': [{
                    'stacked': True
                }]
            }
        },
        'components-linked': False
    }

    stacked_bars = ['contributions',
                    'loans_received',
                    'total_offsets_to_operating_expenditures',
                    'transfers_from_affiliated_committee',
                    'other_receipts']

    for comp in stacked_bars:
        dataset = {
            'label': comp,
            'data': [result[comp]]
        }
        """
        if chart_params['components-linked']:
            dataset['link']
        """
        chart_params['data']['datasets'].append(dataset)
    
    return render_template('single-chart.html',
                           query=cycle + result['candidate_id'], # to update
                           chart_params=chart_params)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
