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

def get_daily_orders(since=None, until=None):
    request_path = 'daily/orders/'
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
        codecs.open('get_daily_orders-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_hourly_gmv(since=None, until=None, last_date=None, next_date=None):
    request_path = 'hourly/gmv/'
    params = []
    #if since is not None:
    if since is not None:
        params.append('since={}'.format(since))
    if until is not None:
        params.append('until={}'.format(until))
    if last_date is not None:
        params.append('last_date={}'.format(last_date))
    if next_date is not None:
        params.append('next_date={}'.format(next_date))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_hourly_gmv-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_newest_tmall_price(product):
    request_path = 'newest/tmall/price'
    params = []
    #if since is not None:
    params.append('product={}'.format(product))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_newest_tmall_price-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_monthly_region_user(since, until):
    request_path = 'monthly/region/user'
    params = []
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
        codecs.open('get_monthly_region_user-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_tmall_industry_trend(third_category=None):
    request_path = 'tmall/industry/trend/'
    params = []
    if third_category is not None:
        params.append('third_category={}'.format(third_category))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_tmall_industry_trend-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_monthly_imported_drug_sales():
    request_path = 'monthly/imported/durg/sales/'
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_monthly_imported_drug_sales-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_daily_top_hundred_gmv(date):
    request_path = 'daily/top/hundred/gmv/'
    params = []
    #if since is not None:
    params.append('date={}'.format(date))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_daily_top_hundred_gmv-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r

def get_daily_orders_origin_gmv(date):
    request_path = 'daily/orders/origin/gmv/'
    params = []
    params.append('date={}'.format(date))
    if params:
        request_path += '?{}'.format('&'.join(params))
    r = api_request(request_path)
    if r.status_code == 200:
        print(r.status_code)
        #print(r.text)
    else:
        print(r.status_code)
        codecs.open('get_garages_daily_orders_sales-error-%s.html' % int(time.time()),
                mode='w', encoding='utf-8').write(r.text)
    return r


class SmokingDashboardAPI(unittest.TestCase):

    def test_get_daily_orders(self):
        name = 'get_garages_daily_orders'
        if name in skipped_targets:
            return
        response = get_daily_orders()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['day', 'returned', 'sls', 'rejected', 'canceled']:
                self.assertTrue(keyword in item)
        self.assertEqual(
                get_daily_orders(since='2015-06-01', until='2017-7-25').status_code,
                200)

    def test_get_hourly_gmv(self):
        name = 'get_hourly_gmv'
        if name in skipped_targets:
            return
        response = get_hourly_gmv()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['user_cnt', 'gmv', 'ords_cnt', 'hour']:
                self.assertTrue(keyword in item)
        self.assertEqual(
                get_hourly_gmv(since='2017-06-01', until='2017-7-25').status_code,
                200)
        last_date='2017-06-01'
        next_date='2017-07-25'
        re_response = get_hourly_gmv(last_date=last_date, next_date=next_date)
        self.assertEqual(re_response.status_code, 200)
        re_data = json.loads(re_response.text)
        self.assertEqual(len(re_data['data'][last_date]), 24)
        self.assertEqual(len(re_data['data'][next_date]), 24)

    def test_get_newest_tmall_price(self):
        name = 'get_newest_tmall_price'
        if name in skipped_targets:
            return
        response = get_newest_tmall_price(product='维生素B12片')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['taobao_id', 'jk_id', 'prod_name', 'shop_name', 'price',
                            'purchase_price', 'margin', 'insert_time']:
                self.assertTrue(keyword in item)

    def test_get_monthly_region_user(self):
        name = 'get_monthly_region_user'
        if name in skipped_targets:
            return
        response = get_monthly_region_user(since='2017-06-01', until='2017-7-25')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['year', 'month', 'region_code',
                            'user_type', 'user_cnt']:
                self.assertTrue(keyword in item)

    def test_get_tmall_industry_trend(self):
        name = 'get_tmall_industry_trend'
        if name in skipped_targets:
            return
        response = get_tmall_industry_trend()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['year', 'week', 'fst_cate', 'scd_cate',
                            'thd_cate', 'trade_index', 'pay_item_qty',
                            'item_cnt', 'avg_trd_idx', 'avg_pay_qty']:
                self.assertTrue(keyword in item)
        self.assertEqual(
                get_tmall_industry_trend(third_category='健脾益肾').status_code,
                200)

    def test_get_monthly_imported_drug_sales(self):
        name = 'get_monthly_imported_drug_sales'
        if name in skipped_targets:
            return
        response = get_monthly_imported_drug_sales()
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['year', 'month', 'sls_impt',
                            'qty_impt', 'sls_ttl', 'qty_ttl', 'impr_per']:
                self.assertTrue(keyword in item)

    def test_get_daily_top_hundred_gmv(self):
        name = 'get_daily_top_hundred_gmv'
        if name in skipped_targets:
            return
        response = get_daily_top_hundred_gmv(date='2017-08-01')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['day', 'product_code', 'gmv',
                            'qty', 'rank']:
                self.assertTrue(keyword in item)

    def test_get_daily_orders_origin_gmv(self):
        name = 'get_daily_orders_origin_gmv'
        if name in skipped_targets:
            return
        response = get_daily_orders_origin_gmv(date='2017-08-01')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(int(response_data['status']), 200)
        self.assertTrue('data' in response_data)
        data = response_data['data']
        for item in data:
            for keyword in ['day', 'origin_type', 'ords_cnt',
                            'gmv', 'user_cnt']:
                self.assertTrue(keyword in item)


if __name__ == '__main__':
    unittest.main()


