import pandas as pd
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import statsmodels.formula.api as smf
import statsmodels.api as sm

from scipy.stats import mstats
from functools import partial

import logging
import pyodbc
import pprint
import importlib

import warnings
warnings.filterwarnings("ignore")

#Define Function-Downloading data from SQL server
def sql2df(query, server, db, user=None, password=None,log_query=False):
    """Execute a SQL query and return results in a formatted DataFrame object
    """
    if log_query:
        logging.info('std.data.sql2df() query: \n' + query)

    if user is not None and password is not None:
        conn_str = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (server, db, user, password)
    else:
        conn_str = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;Trusted_Connection=True' % (server, db)

    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(query, conn)
    return df

"""Download Daily Return Data"""
query = """
    SELECT a.Sedol, s.name AS Name, a.PriceDate, a.TotalReturn,m.security_id AS SecurityID
    FROM FactSet..FactsetStockDaily a
    JOIN intldb..external_id_snapshot_table m
    ON a.Sedol = m.external_id
    AND m.external_id_type = 2 --Sedol vs prod SecurityID Map
    JOIN intldb..security_table s
    ON m.security_id = s.security_id
	JOIN
		( 
		SELECT	SecurityID
		FROM OPENROWSET
       ('SQLNCLI', 'Server=MPQUANT;Trusted_Connection=yes;ADDRESS=MPintlDB,5025;DATABASE=OptMod',		
      '	SELECT	SecurityID
		FROM	OptMod..TM_ProductSecurityTarget
		WHERE	ProductID = 100    ------ USRI: 15965; 
		AND		Target > 0
	   ') 
	   UNION
	   SELECT ConstituentSecurityID as SecurityID
	   From		intldb..BM_FinalWeight b
		WHERE	MarketWeightID = -1
		AND		BenchmarkID = 5    -----1: S&P500; 12: R1 value
	   )t
	 ON s.security_id = t.SecurityID
	 WHERE a.PriceDate > '2012-2-21'
"""
serverName = 'MPQuant,2500'
dbName = 'intldb'
DailyRetData = sql2df(query, server=serverName,db=dbName,user=None,password=None,log_query=True)
DailyRetData.sort_values(['Name', 'PriceDate'], inplace=True)
DailyRetData.reset_index(drop=True, inplace=True)
#%%




df = DailyRetData[['Name', 'PriceDate', 'TotalReturn']].copy()
df.columns = ['Name', 'Date', 'Return']
dates = df.Date.unique()
dates.sort()

    
def compute(df, x):
    df.reset_index(drop=True, inplace=True)
    df['LastDate']=df.groupby('Name')['Date'].transform(np.max).reset_index(drop=True)
    df['LastDateInd'] = (df.Date == df.LastDate)
    
    df_filter = df[(df.Return >= x) & (df.Return <= (x+0.05)) & (df.LastDateInd == False)]
    df_res = df.loc[df_filter.index+1]
    return np.sum(df_res.groupby('Date')['Return'].agg(np.nanmean))


x = np.arange(-0.20, 0.16, 0.01)
y = [compute(df, i) for i in x]
x_optimal = x[np.where(y == max(y))][0].round(2)


record = []
cum_ret = 0
for i, date in enumerate(dates[:-61]):
    print('Training set: from %s to %s' % (dates[i], dates[i+60]))
    dff = df[(df.Date >= dates[i]) & (df.Date <= dates[i+60])]
    x = np.arange(-0.20, 0.16, 0.01)
    y = [compute(dff, i) for i in x]
    x_optimal = x[np.where(y == max(y))][0].round(2)
    
    temp = dff[dff.Date == dates[i+60]]
    selected_stocks = temp[(temp.Return >= x_optimal) & (temp.Return <= (x_optimal+0.05))].Name
    if len(selected_stocks) == 0:
        print('%s: There is no stock being selected based on %s performances' % (dates[i+61], dates[i+60]))
        continue
    else:
        print('%s: There is %i stock(s) being selected' % (dates[i+61], len(selected_stocks)))
        temp = df[(df.Date == dates[i+61]) & (df.Name.isin(selected_stocks))]
        record.append(temp)
        ret = np.nanmean(temp.Return)
        print('\tMean return: %f' % ret)
        cum_ret = (cum_ret+1)*(ret+1) - 1
        print('\tCumulated return: %f' % cum_ret)

test = pd.concat(record)
test = test.groupby('Date')['Return'].agg(np.nanmean)
(test+1).cumprod().plot()
#%%


import pandas as pd
import numpy as np
from datetime import datetime as dt
import os
path = r'C:\Users\LCHEN2\WORKSPACE\China Quant Strat'
os.chdir(path)
from datascraper import investing_api as api


class Backtest:
    def __init__(self, positions, price_exc):
        self.positions = positions
        self.price_exc = price_exc
        self.notional = 10000
    
    def run(self):
        # long table to flat table
        price_mat = pd.pivot_table(data=self.price_exc, index='Time', columns='Asset', values='Price')
        positions_mat = pd.pivot_table(data=self.positions, index='Time', columns='Asset', values='Holdings')
        
        # compute cash value
        val_noncash = (price_mat * positions_mat).sum(axis=1)
        val_noncash_ex = (price_mat * positions_mat.shift()).sum(axis=1)
        val_cash = (val_noncash_ex-val_noncash).cumsum() + self.notional
        
        # compute transaction dollar volume
        transaction_volume = price_mat * (np.abs(positions_mat - positions_mat.shift().fillna(0)))
        
        # total market vale at execution time
        val_total = val_noncash + val_cash
        
        self.value_noncash = val_noncash
        self.value_cash = val_cash
        self.value_total = val_total  
        self.transaction_volume = transaction_volume



api.search('ge') # pairId 8193
df = api.get_data(pair_id='8193', freq='5', start_date=dt(2019,6,15), end_date = dt.utcnow())
df.t = [dt.utcfromtimestamp(x) for x in df.t]


