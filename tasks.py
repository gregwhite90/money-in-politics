import celery
import requests
import os

app = celery.Celery('stay-bought')

redis_url = os.environ.get('REDIS_URL') # to add default?
app.conf.update(broker_url=redis_url,
                result_backend=redis_url)

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