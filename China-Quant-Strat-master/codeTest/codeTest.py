# import modules
import pandas as pd
import numpy as np
import os
import datetime as dt

# set path
Path = r'\\ac2knyc0209\Userdata\LCHEN2\Desktop\China-Quant-Strat-master\China-Quant-Strat-master\codeTest'
os.chdir(Path)
#%%

df = pd.read_csv('codeTest.csv')
df.Pointdate.unique()

df_mkt = pd.read_csv('^GSPC.csv')
df_mkt['Return'] = df_mkt['Adj Close'].pct_change()
df_mkt = df_mkt[['Date', 'Return']]
df_mkt.drop(0, axis=0, inplace=True)
df_mkt.reset_index(drop=True, inplace=True)
df_mkt.rename(columns={'Date': 'Pointdate'}, inplace=True)



def get_rolling_beta(df):
    beta = np.nanprod(df.Return + 1)-1
    return pd.DataFrame({'ID': [df.ID.iloc[0]], 'Pointdate': [df.Pointdate.iloc[0]], 'Beta': [beta]})

df.sort_values(['ID', 'Pointdate'], inplace=True)
test = df.groupby('ID').rolling(window=252, min_periods=189, on='Return').apply(get_rolling_beta)


