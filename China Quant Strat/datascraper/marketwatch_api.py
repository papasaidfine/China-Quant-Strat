# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 12:31:19 2018

@author: lchen2
"""

import requests
import lxml
import pandas as pd
from datetime import datetime as dt
import browsercookie
import json
import warnings

warnings.filterwarnings('ignore')


class MarketWatch:
    def __init__(self):
        self.sample_code = '%7B%22Step%22%3A%22P1D%22%2C%22TimeFrame%22%3A%22P1Y%22%2C%22StartDate%22%3A1514419200000%2C%22EndDate%22%3A1545955200000%2C%22EntitlementToken%22%3A%22cecc4267a0194af89ca343805a3e57af%22%2C%22IncludeMockTick%22%3Atrue%2C%22FilterNullSlots%22%3Afalse%2C%22FilterClosedPoints%22%3Atrue%2C%22IncludeClosedSlots%22%3Afalse%2C%22IncludeOfficialClose%22%3Atrue%2C%22InjectOpen%22%3Afalse%2C%22ShowPreMarket%22%3Afalse%2C%22ShowAfterHours%22%3Afalse%2C%22UseExtendedTimeFrame%22%3Atrue%2C%22WantPriorClose%22%3Afalse%2C%22IncludeCurrentQuotes%22%3Afalse%2C%22ResetTodaysAfterHoursPercentChange%22%3Afalse%2C%22Series%22%3A%5B%7B%22Key%22%3A%22INDEX%2FUS%2FXNAS%2FCOMP%22%2C%22Dialect%22%3A%22Charting%22%2C%22Kind%22%3A%22Ticker%22%2C%22SeriesId%22%3A%22s1%22%2C%22DataTypes%22%3A%5B%22Last%22%5D%2C%22Indicators%22%3A%5B%7B%22Parameters%22%3A%5B%7B%22Name%22%3A%22Period%22%2C%22Value%22%3A%2250%22%7D%5D%2C%22Kind%22%3A%22SimpleMovingAverage%22%2C%22SeriesId%22%3A%22i2%22%7D%2C%7B%22Parameters%22%3A%5B%5D%2C%22Kind%22%3A%22Volume%22%2C%22SeriesId%22%3A%22i3%22%7D%2C%7B%22Parameters%22%3A%5B%7B%22Name%22%3A%22EMA1%22%2C%22Value%22%3A12%7D%2C%7B%22Name%22%3A%22EMA2%22%2C%22Value%22%3A26%7D%2C%7B%22Name%22%3A%22SignalLine%22%2C%22Value%22%3A9%7D%5D%2C%22Kind%22%3A%22MovingAverageConvergenceDivergence%22%2C%22SeriesId%22%3A%22i4%22%7D%5D%7D%5D%7D'
        query = requests.utils.unquote(self.sample_code)
        self.j = json.loads(query)  # edit j in variable explorer
        self.query = json.dumps(self.j)
        self.code = requests.utils.quote(self.query, safe = '')
        self.ckey = 'cecc4267a0'
        self.url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json=' + self.code + '&ckey=' + self.ckey
        
    def refresh_url(self, j):
        self.j = j
        self.query = json.dumps(self.j)
        self.code = requests.utils.quote(self.query, safe = '')
        self.url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json=' + self.code + '&ckey=' + self.ckey

    def get_data(self):        
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
                'Origin': 'https://www.marketwatch.com',
                'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
                }
        
        r = requests.get(self.url, headers = headers, verify = False)
        print('status code: %i' % r.status_code)
        return(r.json())
    
    @classmethod
    def lookup(cls, lookup):
        url = 'https://services.dowjones.com/autocomplete/data'
        params = {'q': lookup}
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
                'Origin': 'https://www.marketwatch.com',
                'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
                }
        r = requests.get(url, cookies = browsercookie.chrome(), headers = headers, params = params, verify = False)
        d = r.json()
        return(d.get('symbols'))


l = MarketWatch.lookup('china csi 300')
l[3]['chartingSymbol']
mktwch = MarketWatch()
mktwch.j['Series'][0]['Key'] = l[3]['chartingSymbol']
mktwch.refresh_url(mktwch.j)
data = mktwch.get_data()





def search(search_text):
    url = 'https://services.dowjones.com/autocomplete/data'
    params = {'q': search_text}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
            'Origin': 'https://www.marketwatch.com',
            'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
            }
    r = requests.get(url, cookies = browsercookie.chrome(), headers = headers, params = params, verify = False)
    print('--- status code: %s ---' % r.status_code)
    j = r.json().get('symbols')
    df = pd.DataFrame(j)
    if df.empty:
        print('No results matched your search')
    else:
        print('Please look up the pairID of your desired security')
        print('Please use UTC time zone')
        return(df)


df = search('chaseasdfasdfa')


sample_code = '%7B%22Step%22%3A%22P1D%22%2C%22TimeFrame%22%3A%22P1Y%22%2C%22StartDate%22%3A1514419200000%2C%22EndDate%22%3A1545955200000%2C%22EntitlementToken%22%3A%22cecc4267a0194af89ca343805a3e57af%22%2C%22IncludeMockTick%22%3Atrue%2C%22FilterNullSlots%22%3Afalse%2C%22FilterClosedPoints%22%3Atrue%2C%22IncludeClosedSlots%22%3Afalse%2C%22IncludeOfficialClose%22%3Atrue%2C%22InjectOpen%22%3Afalse%2C%22ShowPreMarket%22%3Afalse%2C%22ShowAfterHours%22%3Afalse%2C%22UseExtendedTimeFrame%22%3Atrue%2C%22WantPriorClose%22%3Afalse%2C%22IncludeCurrentQuotes%22%3Afalse%2C%22ResetTodaysAfterHoursPercentChange%22%3Afalse%2C%22Series%22%3A%5B%7B%22Key%22%3A%22INDEX%2FUS%2FXNAS%2FCOMP%22%2C%22Dialect%22%3A%22Charting%22%2C%22Kind%22%3A%22Ticker%22%2C%22SeriesId%22%3A%22s1%22%2C%22DataTypes%22%3A%5B%22Last%22%5D%2C%22Indicators%22%3A%5B%7B%22Parameters%22%3A%5B%7B%22Name%22%3A%22Period%22%2C%22Value%22%3A%2250%22%7D%5D%2C%22Kind%22%3A%22SimpleMovingAverage%22%2C%22SeriesId%22%3A%22i2%22%7D%2C%7B%22Parameters%22%3A%5B%5D%2C%22Kind%22%3A%22Volume%22%2C%22SeriesId%22%3A%22i3%22%7D%2C%7B%22Parameters%22%3A%5B%7B%22Name%22%3A%22EMA1%22%2C%22Value%22%3A12%7D%2C%7B%22Name%22%3A%22EMA2%22%2C%22Value%22%3A26%7D%2C%7B%22Name%22%3A%22SignalLine%22%2C%22Value%22%3A9%7D%5D%2C%22Kind%22%3A%22MovingAverageConvergenceDivergence%22%2C%22SeriesId%22%3A%22i4%22%7D%5D%7D%5D%7D'
query = requests.utils.unquote(sample_code)
j = json.loads(query)  # edit j in variable explorer
query = json.dumps(j)
code = requests.utils.quote(query, safe = '')
ckey = 'cecc4267a0'
url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json=' + code + '&ckey=' + ckey
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
        'Origin': 'https://www.marketwatch.com',
        'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
        }

r = requests.get(url, headers = headers, verify = False)
r.status_code

