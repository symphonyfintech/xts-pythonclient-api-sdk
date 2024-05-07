# from XTConnect import XTSConnect
from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io
import numpy as np
import pandas as pd
from datetime import datetime,time

"""Market Data login credentials"""
API_KEY_M = "7e724b496719c0fcff3453"
API_SECRET_M = "Pnog114@9w"
source = "WEBAPI"


"""Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
xtm = XTSConnect(API_KEY_M, API_SECRET_M, source)

"""Using the object we call the login function Request"""
response_m = xtm.marketdata_login()
print("MarketData Login: ", response_m)



# Store the token and userid
set_marketDataToken = response_m['result']['token']
set_muserID = response_m['result']['userID']
print("Login: ", response_m)

exchangesegments = [xtm.EXCHANGE_NSECM, xtm.EXCHANGE_NSEFO]
response = xtm.get_master(exchangeSegmentList=exchangesegments)

with open("FO.txt","w") as file1:
     file1.write(response['result'])

col=['ExchangeSegment','ExchangeInstrumentID','InstrumentType','Name','Description','Series', 'NameWithSeries','InstrumentID','PriceBand.High','PriceBand.Low','FreezeQty','TickSize','LotSize','Multiplier', 'UnderlyingInstrumentId','UnderlyingIndexName','ContractExpiration','StrikePrice','OptionType']
masterdf=pd.read_csv('FO.txt',sep='|',usecols=range(19),header=None,low_memory=False)      
masterdf.columns=col
masterdf=masterdf[(masterdf.UnderlyingIndexName=='NIFTY MID SELECT') ]
masterdf.to_csv('FO.csv', index=False)