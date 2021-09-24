import os
import sys
import requests
import pickle
from operator import itemgetter

def fec_request(endpoint, query):
    fixed_params = {
        'api_key': os.environ.get('DATAGOV_API_KEY'), # to add default?
        'per_page': 100
    }
    payload = {**fixed_params, **query}
    base_uri = 'https://api.open.fec.gov/v1/'
    r = requests.get(base_uri + endpoint, params=payload)
    return r

if __name__ == '__main__':
    if len(sys.argv) < 3:
        # Hillary for America as a default
        committee_type = 'P'
        committee_id = 'C00575795'
    else:
        committee_type = sys.argv[2]
        committee_id = sys.argv[1]
        
    two_year_periods = {
        'P': 2,
        'H': 3,
        'S': 3
    }
    cycle = 2016
    office = 'P'

    sort = 'contribution_receipt_amount'
        
    fec_api_query = {
        'committee_id': committee_id, # to replace with regular function arg
        'is_individual': True,
        'sort': '-' + sort
    }

    total_fec_api_query = {
        'committee_id': committee_id
    }

    last_indexes = ['last_' + sort,
                    'last_index']

    total_itemized_contributions = 0.0
    
    aggregate_contributions = {}

    for two_year_offset in range(two_year_periods[office]):
        two_year_transaction_period = cycle - 2 * two_year_offset
        print('---Two Year Period: %d---' % two_year_transaction_period)

        fec_api_query['two_year_transaction_period'] = two_year_transaction_period
        total_fec_api_query['cycle'] = two_year_transaction_period
        
        for idx_tracker in last_indexes: fec_api_query.pop(idx_tracker, None)
        
        total_response = fec_request('totals/' + committee_type + '/',
                                     total_fec_api_query)

        if (total_response.status_code == requests.codes.ok and
            'results' in total_response.json() and
            len(total_response.json()['results']) == 1):
            
            total_itemized_contributions += total_response.json()['results'][0]['individual_itemized_contributions']
            
        query_response = fec_request('schedules/schedule_a/',
                                     fec_api_query)

        print('\n---%s queries remaining---\n' % query_response.headers['X-RateLimit-Remaining'])
        
        while not len(query_response.json()['results']) == 0:
            results = query_response.json()['results']
            for result in results:
                aggregate_contributions[result['contributor_name']] = aggregate_contributions.get(result['contributor_name'], 0.0) + result['contribution_receipt_amount']
                print('%s contributed %f. Aggregate: %f' % (result['contributor_name'],
                                                            result['contribution_receipt_amount'],
                                                            aggregate_contributions[result['contributor_name']]))
            for idx_tracker in last_indexes:
                fec_api_query[idx_tracker] = query_response.json()['pagination']['last_indexes'][idx_tracker]

            query_response = fec_request('schedules/schedule_a/',
                                         fec_api_query)

            print('\n---%s queries remaining---\n' % query_response.headers['X-RateLimit-Remaining'])

            
    print('-----total aggregated contributions-----')
    
    for contributor_name, aggregate_contribution in sorted(aggregate_contributions.items(),
                                                           key=itemgetter(1),
                                                           reverse=True):
        print('%s: %f' % (contributor_name, aggregate_contribution))
    print('total check:\n%f\n%f' % (sum(aggregate_contributions.values()),
                                    total_itemized_contributions))
