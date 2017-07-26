# encoding:utf8

import requests
import urllib
import json
import time
import random
import hmac
import hashlib

DEBUG = False


def sig(method, url, access_key, secret_key,
        timestamp=None, nonce=None, sig_method='HMAC-SHA1'):
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    if nonce is None:
        nonce = random.random()
    seperator = '?' in url and '&' or '?'
    url = '%s%saccess_key=%s&timestamp=%s&nonce=%s' \
            % (url, seperator, access_key, timestamp, nonce)
    quoted_url = urllib.parse.quote('%s %s' % (method, url), safe='')
    if sig_method == 'HMAC-SHA1':
        return timestamp, nonce, hmac.new(\
                bytearray(secret_key, 'ASCII'), bytearray(quoted_url, 'ASCII'),
                hashlib.sha256)\
                        .hexdigest().strip()

def api_request(path,
        data=None,
        json=None,
        protocol='http',
        host='127.0.0.1',
        port=8888,
        prefix='/v1',
        method='GET',
        access_key=None,
        secret_key=None):
    if DEBUG:
        print('api_request: data=%s' % data)
    method = method or data and 'POST' or 'GET'
    url = '%s://%s:%s%s/%s' \
            % (protocol, host, port,
                    prefix, path)
    if access_key is not None and secret_key is not None:
        timestamp, nonce, signature = sig(method, url, access_key, secret_key)
        if DEBUG:
            print(timestamp, nonce, signature)
        seperator = '?' in url and '&' or '?'
        url = '%s%saccess_key=%s&timestamp=%s&nonce=%s&sig=%s' \
                % (url, seperator, access_key, timestamp, nonce, signature)
    print('url=', url)
    if not data and not json:
        r = requests.get(url)
    else:
        r = requests.post(url, data=data, json=json)

    if DEBUG:
        print('-'*20, url)
        print(r.status_code)
        if 200 == r.status_code:
            print(r.text)
            print(r.json())

    return r
