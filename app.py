from flask import Flask, render_template, url_for
import tasks

app = Flask(__name__)

solarized_base_colors = [
    '#002b36', # base03 
    '#073642', # base02 
    '#586e75', # base01 
    '#657b83', # base00 
    '#839496', # base0  
    '#93a1a1', # base1  
    '#eee8d5', # base2  
    '#fdf6e3' # base3     
]

solarized_accent_colors = [
    '#b58900', # yellow
    '#cb4b16', # orange
    '#dc322f', # red
    '#d33682', # magenta
    '#6c71c4', # violet
    '#268bd2', # blue
    '#2aa198', # cyan
    '#859900'  # green
]

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

    stacked_bars = ['total_receipts']
    
    chart_params = {
        'type': 'bar',
        'data': {
            'labels': [],
            'links': [],
            'datasets': [{
                'label': stacked_bar,
                'data': [],
                'backgroundColor': solarized_base_colors[idx]
            } for idx, stacked_bar in enumerate(stacked_bars)]
        },
        'components-linked': True
    }

    min_receipts = 5000000.0
    max_candidates = 5

    for idx, result in enumerate(query_response.json()['results']):
        if result[stacked_bars[0]] < min_receipts or idx >= max_candidates:
            break
        chart_params['data']['labels'].append(result['candidate_name'])
        chart_params['data']['links'].append(
            url_for('candidate_summary',
                    candidate_fec_id=result['candidate_id']))
        for bar_idx, bar in enumerate(stacked_bars):
            chart_params['data']['datasets'][bar_idx]['data'].append(result[bar])
    
    return render_template('single-chart.html',
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

    for idx, comp in enumerate(stacked_bars):
        dataset = {
            'label': comp,
            'data': [result[comp]],
            'backgroundColor': solarized_base_colors[idx]
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
