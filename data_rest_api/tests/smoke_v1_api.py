#coding:utf-8

import codecs
import json
import time

import unittest

from remote_common import api_request as _api_request

from smoke_dashboard_api_settings import DEBUG, \
        ACCESS_KEY, \
        SECRET_KEY, \
        JIANKE_PROTOCOL, \
        JIANKE_HOST, \
        JIANKE_PORT, \
        JIANKE_API_PREFIX, \
        skipped_targets

def api_request(path, data=None, json=None, method=None):
    return _api_request(path,
            protocol=JIANKE_PROTOCOL,
            host=JIANKE_HOST,
            port=JIANKE_PORT,
            prefix=JIANKE_API_PREFIX,
            data=data,
            json=json,
            method=method,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY)

def get_orders_log_per_day(since=None, until=None):
    request_path = 'orders/day/'
    params = []
    #if since is not None:
    if since is not None:
        params.append('since={}'.format(since))
    if until is not None:
        params.append('until={}'.format(until))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_orders_log_per_day-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r


class SmokingDashboardAPI(unittest.TestCase):

    def test_get_orders_log_per_day(self):
        name = 'get_garages_orders_log_per_day'
        if name in skipped_targets:
            return
        response = get_orders_log_per_day()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            self.assertTrue('date' in item)
            self.assertTrue('unconfirmed' in item)
        self.assertEqual(
                get_orders_log_per_day(since='2015-06-01', until='2017-7-25').status_code,
                200)


if __name__ == '__main__':
    unittest.main()


