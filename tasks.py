import celery
import requests
import os

app = celery.Celery('stay-bought')

@app.task
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

redis_url = os.environ.get('REDIS_URL') # to add default?

app.conf.update(BROKER_URL=redis_url,
                CELERY_RESULT_BACKEND=redis_url)
