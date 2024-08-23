import json
import logging
import urllib3

logger = logging.getLogger()

retry = urllib3.Retry(total = 20, backoff_factor=1)

def do_request(method, endpoint, **kwargs):
    http = urllib3.PoolManager(retries = retry)

    if method == 'GET' and 'params' in kwargs:
        params = kwargs.get('params')
        endpoint = endpoint + ("?" + urllib3.request.urlencode(params) if params is not None else "")

    req_params = {}

    if 'headers' in kwargs:
        req_params['headers'] = kwargs.get('headers')

    if method in ['POST','PUT']:
        if 'json' in kwargs:
            req_params['body'] = json.dumps(kwargs.get('json'))
        elif 'data' in kwargs:
            req_params['body'] = kwargs.get('data')
    try:
        raw_response = http.urlopen(method, endpoint, **req_params)
        res = HttpResponse(raw_response)

        if res.status_code < 200 or res.status_code >= 300:
            logger.info(endpoint)
            logger.info(res.status_code)
            logger.info(res.text)
        
        return res
    except Exception as e:
        print(endpoint)
        print(e)
        return ""
    

def get(endpoint, **kwargs):
    return do_request('GET', endpoint, **kwargs)
    
class HttpResponse:
    def __init__(self, response):
        self._response = response
        self.status_code = response.status
        try:
            self.text = response.data.decode('utf-8')
        except Exception as e:
            logger.error(e)
            self.text = str(response.data)

    def json(self):
        return json.loads(self.text)