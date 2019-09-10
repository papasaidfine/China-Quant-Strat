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
        print('Initializing query ... ')
        sample_code = '{"Step":"PT1M","TimeFrame":"D5","StartDate":1568073600000,"EndDate":1568073600000,"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":true,"FilterNullSlots":false,"FilterClosedPoints":true,"IncludeClosedSlots":false,"IncludeOfficialClose":true,"InjectOpen":false,"ShowPreMarket":false,"ShowAfterHours":false,"UseExtendedTimeFrame":true,"WantPriorClose":false,"IncludeCurrentQuotes":false,"ResetTodaysAfterHoursPercentChange":false,"Series":[{"Key":"INDEX/US/S&P US/SPX","Dialect":"Charting","Kind":"Ticker","SeriesId":"s1","DataTypes":["Open","High","Low","Last"],"Indicators":[{"Parameters":[],"Kind":"Volume","SeriesId":"i3"}]}]}'
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
        print('OK')

    def get_data(self):        
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
                'Origin': 'https://www.marketwatch.com',
                'Referer': 'https://www.marketwatch.com/investing/stock/aapl/charts'
                }
        
        print('Requesting data ... ')
        r = requests.get(self.url, headers = headers, verify = False)
        print('status code: %i' % r.status_code)
        
        data = r.json()
        df = pd.DataFrame()
        for i in range(len(data['Series'])):
            df[data['Series'][i]['DesiredDataPoints']] = pd.DataFrame(data['Series'][i]['DataPoints'])
        t = [dt.fromtimestamp(x/1000) for x in data['TimeInfo']['Ticks']]
        df['t'] = t
        df.set_index('t', inplace=True)
        self.raw = data
        print('OK')
        
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








#%%
## for debug

sample_code = '{"Step":"P1D","TimeFrame":"P1Y","StartDate":1536537600000,"EndDate":1568073600000,"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":true,"FilterNullSlots":false,"FilterClosedPoints":true,"IncludeClosedSlots":false,"IncludeOfficialClose":true,"InjectOpen":false,"ShowPreMarket":false,"ShowAfterHours":false,"UseExtendedTimeFrame":true,"WantPriorClose":false,"IncludeCurrentQuotes":false,"ResetTodaysAfterHoursPercentChange":false,"Series":[{"Key":"INDEX/US/DOW JONES GLOBAL/DJIA","Dialect":"Charting","Kind":"Ticker","SeriesId":"s1","DataTypes":["Open","High","Low","Last"],"Indicators":[{"Parameters":[{"Name":"Period","Value":"50"}],"Kind":"SimpleMovingAverage","SeriesId":"i2"},{"Parameters":[],"Kind":"Volume","SeriesId":"i3"},{"Parameters":[{"Name":"EMA1","Value":12},{"Name":"EMA2","Value":26},{"Name":"SignalLine","Value":9}],"Kind":"MovingAverageConvergenceDivergence","SeriesId":"i4"},{"Parameters":[{"Name":"Period","Value":12}],"Kind":"Momentum","SeriesId":"i5"}]}]}'
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










