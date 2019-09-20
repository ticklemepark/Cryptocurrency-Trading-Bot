import time
import hmac
import hashlib
import sys
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from Crypto.Cipher import AES
except ImportError:
    encrypted = False
else:
    import getpass
    import ast
    import json

    encrypted = True

import requests



def encrypt(api_key, api_secret, export=True, export_fn='secrets.json'):
    cipher = AES.new(getpass.getpass(
        'Input encryption password (string will not show)'))
    api_key_n = cipher.encrypt(api_key)
    api_secret_n = cipher.encrypt(api_secret)
    api = {'key': str(api_key_n), 'secret': str(api_secret_n)}
    if export:
        with open(export_fn, 'w') as outfile:
            json.dump(api, outfile)
    return api


def using_requests(request_url, apisign):
    return requests.get(
        request_url,
        headers={"apisign": apisign},
        timeout=10
    ).json()


class Bittrex(object):
    """
    Used for requesting Bittrex with API key and API secret
    """

    def __init__(self, api_key, api_secret, calls_per_second=1, dispatch=using_requests, api_version=API_V1_1):
        self.api_key = str(api_key) if api_key is not None else ''
        self.api_secret = str(api_secret) if api_secret is not None else ''
        self.dispatch = dispatch
        self.call_rate = 1.0 / calls_per_second
        self.last_call = None
        self.api_version = api_version

    def decrypt(self):
        if encrypted:
            cipher = AES.new(getpass.getpass(
                'Input decryption password (string will not show)'))
            try:
                if isinstance(self.api_key, str):
                    self.api_key = ast.literal_eval(self.api_key)
                if isinstance(self.api_secret, str):
                    self.api_secret = ast.literal_eval(self.api_secret)
            except Exception:
                pass
            self.api_key = cipher.decrypt(self.api_key).decode()
            self.api_secret = cipher.decrypt(self.api_secret).decode()
        else:
            raise ImportError('"pycrypto" module has to be installed')

    def wait(self):
        if self.last_call is None:
            self.last_call = time.time()
        else:
            now = time.time()
            passed = now - self.last_call
            if passed < self.call_rate:
                # print("sleep")
                time.sleep(self.call_rate - passed)

            self.last_call = time.time()

    def _api_query(self, protection=None, path_dict=None, options=None):
        """
        Queries Bittrex
        :param request_url: fully-formed URL to request
        :type options: dict
        :return: JSON response from Bittrex
        :rtype : dict
        """

        if not options:
            options = {}

        if self.api_version not in path_dict:
            raise Exception('method call not available under API version {}'.format(self.api_version))

        request_url = BASE_URL_V2_0 if self.api_version == API_V2_0 else BASE_URL_V1_1
        request_url = request_url.format(path=path_dict[self.api_version])

        nonce = str(int(time.time() * 1000))

        if protection != PROTECTION_PUB:
            request_url = "{0}apikey={1}&nonce={2}&".format(request_url, self.api_key, nonce)

        request_url += urlencode(options)

        try:
            if sys.version_info >= (3, 0) and protection != PROTECTION_PUB:

                apisign = hmac.new(bytearray(self.api_secret, 'ascii'),
                                   bytearray(request_url, 'ascii'),
                                   hashlib.sha512).hexdigest()

            else:

                apisign = hmac.new(self.api_secret.encode(),
                                   request_url.encode(),
                                   hashlib.sha512).hexdigest()

            self.wait()

            return self.dispatch(request_url, apisign)

        except Exception:
            return {
                'success': False,
                'message': 'NO_API_RESPONSE',
                'result': None
            }


    def get_balance (self, cur = ''):
		nonce = self.get_nonce()
		reqUrl = self._ReqUrlDict['GET_BALANCES'].format(no = nonce) if cur is '' else self._ReqUrlDict['GET_BALANCE'].format (no = nonce, cur = cur)
		return self.get_json (reqUrl, self.hmac_sign (reqUrl, self._secret))

    def get_currencies(self):
        return self._api_query(path_dict={
            API_V1_1: '/public/getcurrencies',
            API_V2_0: '/pub/Currencies/GetCurrencies'
        }, protection=PROTECTION_PUB)

    def get_ticker(self, market):
        return self._api_query(path_dict={
            API_V1_1: '/public/getticker',
        }, options={'market': market}, protection=PROTECTION_PUB)

    def get_market_summary(self, market):
        return self._api_query(path_dict={
            API_V1_1: '/public/getmarketsummary',
            API_V2_0: '/pub/Market/GetMarketSummary'
        }, options={'market': market, 'marketname': market}, protection=PROTECTION_PUB)

    def get_market_history(self, market):
        return self._api_query(path_dict={
            API_V1_1: '/public/getmarkethistory',
        }, options={'market': market, 'marketname': market}, protection=PROTECTION_PUB)

    def buy_limit(self, market, quantity, rate):
        return self._api_query(path_dict={
            API_V1_1: '/market/buylimit',
        }, options={'market': market,
                    'quantity': quantity,
                    'rate': rate}, protection=PROTECTION_PRV)

    def sell_limit(self, market, quantity, rate):
        return self._api_query(path_dict={
            API_V1_1: '/market/selllimit',
        }, options={'market': market,
                    'quantity': quantity,
                    'rate': rate}, protection=PROTECTION_PRV)

    def cancel(self, uuid):
        return self._api_query(path_dict={
            API_V1_1: '/market/cancel',
            API_V2_0: '/key/market/tradecancel'
        }, options={'uuid': uuid, 'orderid': uuid}, protection=PROTECTION_PRV)
