import pandas as pd
import numpy as np
import requests
from datetime import datetime as dt
import time


## search for pairId of your desired security
def search(search_text):    
    url = 'https://www.investing.com/search/service/searchTopBar'
    headers = {
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Host': 'www.investing.com'
               }
    data = {'search_text': search_text}    
    r = requests.post(url, headers=headers, data = data)
    print('--- status code: %s ---' % r.status_code)
    dict_list = r.json()['quotes']
    df = pd.DataFrame.from_dict(dict_list)
    if df.empty:
        print('No results matched your search')
    else:
        print('Please look up the pairID of your desired security')
        print('Please use UTC time zone')
        print('''
# an example:
srch = search('601618')
start_date = dt(2018,1,1)
end_date = dt.utcnow()
pair_id = '166'  # pair id of the stock or security
freq = 'D'  # data frequency, {5 min: 5, 15 min: 15, 1 hour: 60, 5 hours: 300, ..., 1 day: D, 1 week: W, 1 month: M}
df = get_data(pair_id=pair_id, freq=freq)
df.t = [dt.utcfromtimestamp(x) for x in df.t]
        ''')        
        return(df[['pairId', 'name', 'flag', 'exchange', 'pair_type']])


## download data from investing.com
def get_data(pair_id, freq, start_date=dt(2000,1,1), end_date=dt.utcnow()):
    print('Request data')
    s = str(int(start_date.timestamp()))  # start date
    e = str(int(end_date.timestamp()))  # end date
    url = 'https://tvc4.forexpros.com/1933f6877141af85d05a53dbb0faf7f6/1550612080/1/1/8/history?' + 'symbol='+pair_id + '&resolution='+freq + '&from='+s + '&to='+e
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    start_time = time.time()
    r = requests.get(url, headers=headers)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('--- status code: %s ---' % r.status_code)
    j = r.json()
    df = pd.DataFrame(j)
    print('... OK')
    return(df)

## example
#srch = search('601618')
#start_date = dt(2018,1,1)
#end_date = dt.utcnow()
#pair_id = '166'  # pair id of the stock or security
#freq = 'D'  # data frequency, {5 min: 5, 15 min: 15, 1 hour: 60, 5 hours: 300, ..., 1 day: D, 1 week: W, 1 month: M}
#df = get_data(pair_id=pair_id, freq=freq)
#df.t = [dt.utcfromtimestamp(x) for x in df.t]


