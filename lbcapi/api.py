import datetime
import hashlib
import hmac as hmac_lib
import requests
import sys
import time
from datetime import datetime
from urllib.parse import urlparse
from db import db

dbExecutor = db.dbExecutor

domain = dbExecutor.read_settings_single('domain')

local_url = 'https://localbitcoins.' + domain


def internet_on():
    try:
        response = requests.get(local_url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False


def hmac(hmac_key, hmac_secret, server=local_url):

    conn = Connection()
    conn._set_hmac(server, hmac_key, hmac_secret)
    return conn


class Connection():
    def __init__(self):
        self.server = None
        # HMAC stuff
        self.hmac_key = None
        self.hmac_secret = None

    def microtime(self, get_as_float=False):
        d = datetime.now()
        t = time.mktime(d.timetuple())
        if get_as_float:
            return t
        else:
            ms = d.microsecond / 1000000.
            return '%f %d' % (ms, t)

    def nonce(self):
        mt = self.microtime().split(' ')
        mt1 = mt[1]
        mt2 = int(float(mt[0]) * 1000000)
        nonce = f'{mt1}{mt2}'
        return nonce

    def call(self, method, url, params=None, stream=False, files=None):
        # improvisation of delayer
        time.sleep(1)

        method = method.upper()
        if method not in ['GET', 'POST']:
            raise Exception(u'Invalid method {}!'.format(method))

        if method == 'GET' and files:
            raise Exception(u'You cannot send files with GET method!')

        if files and not isinstance(files, dict):
            raise Exception(
                u'"files" must be a dict of file objects or file contents!')

        # If URL is absolute, then convert it
        if url.startswith(self.server):
            url = url[len(self.server):]

        # If HMAC
        elif self.hmac_key:

            # If nonce fails, retry several times, then give up
            for retry in range(10):

                # nonce = str(int(time.time() * 1000)).encode('ascii')
                nonce = self.nonce().encode('ascii')
                # Prepare request based on method.
                if method == 'POST':
                    api_request = requests.Request(
                        'POST', self.server + url, data=params, files=files).prepare()
                    params_encoded = api_request.body

                # GET method
                else:
                    api_request = requests.Request(
                        'GET', self.server + url, params=params).prepare()
                    params_encoded = urlparse(api_request.url).query

                # Calculate signature
                message = nonce + self.hmac_key + url.encode('ascii')
                if params_encoded:
                    if sys.version_info >= (3, 0) and isinstance(params_encoded, str):
                        message += params_encoded.encode('ascii')
                    else:
                        message += params_encoded
                signature = hmac_lib.new(
                    self.hmac_secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

                # Store signature and other stuff to headers
                api_request.headers['Apiauth-Key'] = self.hmac_key
                api_request.headers['Apiauth-Nonce'] = nonce
                api_request.headers['Apiauth-Signature'] = signature

                # Send request
                session = requests.Session()
                response = session.send(api_request, stream=stream)

                # If HMAC Nonce is already used, then wait a little and try again
                try:
                    response_json = response.json()
                    if int(response_json.get('error', {}).get('error_code')) == 42:
                        # time.sleep(0.1)
                        continue
                except:
                    # No JSONic response, or interrupt, better just give up
                    pass

                return response

            raise Exception(u'Nonce is too small!')

    def _set_hmac(self, server, hmac_key, hmac_secret):
        self.server = server
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.hmac_key = hmac_key.encode('ascii')
        self.hmac_secret = hmac_secret.encode('ascii')


def get_profile_ads(conn):  # get all ads from localbitcoins profile
    return conn.call('GET', '/api/ads/').json()


def get_profile_ad(conn, ad_id):  # get one concrete ad from localbitcoins profile
    data = conn.call('GET', '/api/ad-get/' +
                     str(ad_id)+'/').json()
    return data['data']['ad_list'][0]['data']


def price_eq(conn, ad_id, price_val):  # send new price to concrete ad
    params = {'price_equation': price_val}
    return conn.call('POST', '/api/ad-equation/' +
                             str(ad_id)+'/', params)


def payment_methods(conn):
    return conn.call('GET', '/api/payment_methods/').json()


def get_ad_list(conn, method_url):  # get ad list asccording to bot specifics
    data = conn.call('GET', method_url).json()
    return data


# check the file size (before downloading) works weird...  always 114
def check_file_size(conn, bot_set):
    with conn.call('GET',  '/' + bot_set['method_url']) as url:
        return url.headers['Content-Length']
        # sreturn url.headers


def get_open_trades(conn):
    return conn.call('GET', '/api/dashboard/').json()


def send_message(conn, contact_id, message):
    conn.call('POST', '/api/contact_message_post/' +
              str(contact_id) + '/', {'msg': str(message)})

# curr1 - sell ceuurency, curr2 - buy currency


def get_fiat_currency_rates(curr1, curr2):
    if str(curr1.lower()) == str(curr2.lower()):
        return 1
    curr2 = curr2.lower()
    url = 'http://www.floatrates.com/daily/' + curr2 + '.json'
    resp = requests.get(url)
    resp = resp.json()
    curr1 = curr1.lower()
    rate = resp[curr1]["rate"]
    return round(rate, 3)
