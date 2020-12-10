import configparser
import json
import os
import csv
from datetime import datetime
from threading import Thread
from MarketDataSocketClient import MDSocket_io
from Connect import XTSConnect
from csv import writer
import asyncio


# MarketData API Credentials
API_KEY = "c2368d9aabcafe7a3e8529"
API_SECRET = "Xogi551#V5"
source = "WEBAPI"

# Initialise
xt = XTSConnect(API_KEY, API_SECRET, source)

# Login for authorization token
response = xt.marketdata_login()

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']
print("Login: ", response)

# Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID)

# Instruments for subscribing
Instruments = [{'exchangeSegment': 51, 'exchangeInstrumentID': 217512}]

# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

    # Subscribe to instruments
    response = xt.send_subscription(Instruments, 1501)
    print("res: ", response)


# Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print('I received a 1502 Market depth message!' + data)
    message = "1502 >> #{id} >> {data}".format(id=2885, data=data)
    sock.send(message)

# Callback for message code 1504 FULL
def on_message1504_json_full(data):
    print('I received a 1504 Index data message!' + data)

# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    print('I received a 1510 Level1,Touchline message!' + data)
    message = "1501 >> #{id} >> {data}".format(id=2885, data=data)
    sock.send(message)

# Callback for message code 1502 PARTIAL
def on_message1502_json_partial(data):
    print('I received a 1502 partial message!' + data)

# Callback for message code 1504 PARTIAL
def on_message1504_json_partial(data):
    print('I received a 1504 Index data message!' + data)

# Callback for message code 1505 PARTIAL
def on_message1505_json_partial(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1510 PARTIAL
def on_message1510_json_partial(data):
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    now = datetime.now()
    today = now.strftime("%H:%M:%S")
    print(today, 'in main 1501 partial Level1,Touchline message!' + data + ' \n')
    print('I received a 1510 Level1,Touchline message!' + data)

# Callback for disconnection
def on_disconnect():
    print('Market Data Socket disconnected!')

# Callback for error
def on_error(data):
    """Error from the socket."""
    print('Market Data Error', data)


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_message1502_json_full = on_message1502_json_full
soc.on_message1504_json_full = on_message1504_json_full
soc.on_message1505_json_full = on_message1505_json_full
soc.on_message1510_json_full = on_message1510_json_full
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1502_json_partial = on_message1502_json_partial
soc.on_message1504_json_partial = on_message1504_json_partial
soc.on_message1505_json_partial = on_message1505_json_partial
soc.on_message1510_json_partial = on_message1510_json_partial
soc.on_message1501_json_partial = on_message1501_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error

# Event listener
el = soc.get_emitter()
el.on('Socket Connection', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()