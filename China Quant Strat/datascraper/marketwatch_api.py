import requests
import lxml
import pandas as pd
from datetime import datetime as dt
import browsercookie
import json
import warnings

warnings.filterwarnings('ignore')


class MarketWatch:
    def __init__(self, chartingSymbol = 'STOCK/US/XNYS/GE', TimeFrame = 'D10', Step = 'PT1M', StartDate = dt(2019,9,9), EndDate = dt(2019,9,9)):
        sample_code = '{"Step":"PT1M","TimeFrame":"D10","StartDate":1567987200000,"EndDate":1567987200000,"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":true,"FilterNullSlots":false,"FilterClosedPoints":true,"IncludeClosedSlots":false,"IncludeOfficialClose":true,"InjectOpen":false,"ShowPreMarket":false,"ShowAfterHours":false,"UseExtendedTimeFrame":true,"WantPriorClose":false,"IncludeCurrentQuotes":false,"ResetTodaysAfterHoursPercentChange":false,"Series":[{"Key":"STOCK/US/XNYS/GE","Dialect":"Charting","Kind":"Ticker","SeriesId":"s1","DataTypes":["Open","High","Low","Last"],"Indicators":[{"Parameters":[],"Kind":"Volume","SeriesId":"i3"}]}]}'
        query = requests.utils.unquote(sample_code)
        j = json.loads(query)  # edit j in variable explorer
        
        j['Series'][0]['Key'] = chartingSymbol
        j['Step'] = Step
        j['TimeFrame'] = TimeFrame
        j['StartDate'] = int(dt.timestamp(StartDate)*1000)
        j['EndDate'] = int(dt.timestamp(EndDate)*1000)
            
        query = json.dumps(j)
        code = requests.utils.quote(query, safe = '')
        ckey = 'cecc4267a0'
        self.url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json=' + code + '&ckey=' + ckey
        

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
        
        data = r.json()
        t = [dt.fromtimestamp(x/1000) for x in data['TimeInfo']['Ticks']]
        v = pd.DataFrame(data['Series'][1]['DataPoints'])
        df = pd.DataFrame(data['Series'][0]['DataPoints'])
        df.columns = ['o', 'h', 'l', 'c']
        df['t'] = t
        df['v'] = v
        df.set_index('t', inplace=True)

        return(df)
    
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
        print('Find the chartingSymbol for the security.')
        print('''
l = MarketWatch.lookup('wuliangye')

## TimeFrame: 1D: 'D1', 10D: 'D10', 1M: 'P29D', 3M: 'P3M', 1Y: 'P1Y', ..., All: 'all'
## Step: 5Min: 'PT5M', 1Hour: 'PT1H', Daily: 'P1D', Weekly: 'P7D', Monthly: 'P1M'
mktwch = MarketWatch(chartingSymbol='STOCK/CN/XSHE/000858', TimeFrame = 'D10', Step = 'PT1M', StartDate = dt(2019,9,9), EndDate = dt(2019,9,9))
data = mktwch.get_data()
                ''')
        return(d.get('symbols'))



l = MarketWatch.lookup('wuliangye')

## TimeFrame: 1D: 'D1', 10D: 'D10', 1M: 'P29D', 3M: 'P3M', 1Y: 'P1Y', ..., All: 'all'
## Step: 5Min: 'PT5M', 1Hour: 'PT1H', Daily: 'P1D', Weekly: 'P7D', Monthly: 'P1M'
mktwch = MarketWatch(chartingSymbol='STOCK/CN/XSHG/600519', TimeFrame = 'D10', Step = 'PT1M', StartDate = dt(2019,9,9), EndDate = dt(2019,9,9))
data = mktwch.get_data()




#%%
## for debug

sample_code = '{"Step":"PT1M","TimeFrame":"D10","StartDate":1567987200000,"EndDate":1567987200000,"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":true,"FilterNullSlots":false,"FilterClosedPoints":true,"IncludeClosedSlots":false,"IncludeOfficialClose":true,"InjectOpen":false,"ShowPreMarket":false,"ShowAfterHours":false,"UseExtendedTimeFrame":true,"WantPriorClose":false,"IncludeCurrentQuotes":false,"ResetTodaysAfterHoursPercentChange":false,"Series":[{"Key":"STOCK/US/XNYS/GE","Dialect":"Charting","Kind":"Ticker","SeriesId":"s1","DataTypes":["Open","High","Low","Last"],"Indicators":[{"Parameters":[],"Kind":"Volume","SeriesId":"i3"}]}]}'
query = requests.utils.unquote(sample_code)
j = json.loads(query)  # edit j in variable explorer

j['Series'][0]['Key'] = 'STOCK/US/XNYS/GE'
j['Step'] = 'PT1M'
j['TimeFrame'] = 'D10'
j['StartDate'] = int(dt.timestamp(dt(2019,9,9))*1000)
j['EndDate'] = int(dt.timestamp(dt(2019,9,9))*1000)

headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
                'Origin': 'https://www.marketwatch.com',
                'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
                }
        
    
query = json.dumps(j)
code = requests.utils.quote(query, safe = '')
ckey = 'cecc4267a0'
url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json=' + code + '&ckey=' + ckey

r = requests.get(url, headers = headers, verify = False)
r.status_code
data = r.json()



















#def search(search_text):
#    url = 'https://services.dowjones.com/autocomplete/data'
#    params = {'q': search_text}
#    headers = {
#            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#            'Accept': 'application/json, text/javascript, */*; q=0.01',
#            'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
#            'Origin': 'https://www.marketwatch.com',
#            'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
#            }
#    r = requests.get(url, cookies = browsercookie.chrome(), headers = headers, params = params, verify = False)
#    print('--- status code: %s ---' % r.status_code)
#    j = r.json().get('symbols')
#    df = pd.DataFrame(j)
#    if df.empty:
#        print('No results matched your search')
#    else:
#        print('Please look up the pairID of your desired security')
#        print('Please use UTC time zone')
#        return(df)










