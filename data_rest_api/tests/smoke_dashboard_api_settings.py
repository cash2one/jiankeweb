# encoding:utf8

DEBUG = False

ACCESS_KEY = '10002'
SECRET_KEY = '161352e34a48498884c8927192b57c90'

JIANKE_PROTOCOL = 'http'
JIANKE_HOST = '127.0.0.1'
JIANKE_PORT = 8888
JIANKE_API_PREFIX = '/v1'


skipped_targets = (
    'get_daily_orders',
    'get_hourly_gmv',
    'get_newest_tmall_price',
    'get_monthly_region_user',
    'get_tmall_industry_trend',
    'get_monthly_imported_drug_sales',
    'get_daily_top_hundred_gmv',
    )

# vim: filetype=python
