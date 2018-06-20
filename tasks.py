import celery
import requests
import os

app = celery.Celery('stay-bought')

@app.task
def fec_request(endpoint, query):
    fixed_params = {
        'api_key': os.environ.get('DATAGOV_API_KEY'), # to add default?
        'per_page': 100,
        'page': 1
    }
    payload = {**fixed_params, **query}
    base_uri = 'https://api.open.fec.gov/v1/'
    r = requests.get(base_uri + endpoint, params=payload)
    return r

@app.task
def pp_cf_request(endpoint):
    headers = {
        'X-API-Key': os.environ.get('PROPUBLICA_CAMPAIGN_FINANCE_API_KEY')
    }
    data_format = '.json'
    base_uri = 'https://api.propublica.org/campaign-finance/v1/'
    r = requests.get(base_uri + endpoint + data_format, headers=headers)
    return r

redis_url = os.environ.get('REDIS_URL') # to add default?

app.conf.update(BROKER_URL=redis_url,
                CELERY_RESULT_BACKEND=redis_url)
