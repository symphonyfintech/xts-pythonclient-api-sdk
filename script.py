from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import random
import time
import requests
import json

"Note : For dealer credentials add the clientID and for investor client leave the clientID blank"

"""InVestor credentials"""
API_KEY = "48fea59dfc71428ba1a335"
API_SECRET = "Atei167#ys"
source = "WEBAPI"

"""Market Data login credentials"""
API_KEY_M = "7e724b496719c0fcff3453"
API_SECRET_M = "Pnog114@9w"
source = "WEBAPI"

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the xt object we created call the interactive login Request"""
response_o = xt.interactive_login()
print("Login: ", response_o)
"""Order book Request"""
response_o = xt.get_order_book()
print("Order Book: ", response_o)



"""Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
xtm = XTSConnect(API_KEY_M, API_SECRET_M, source)

"""Using the object we call the login function Request"""
response_m = xtm.marketdata_login()
print("MarketData Login: ", response_m)



# Store the token and userid
set_marketDataToken = response_m['result']['token']
set_muserID = response_m['result']['userID']
print("Login: ", response_m)

# Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID)

# Instruments for subscribing
Instruments = [
           #     {'exchangeSegment': xt.EXCHANGE_NSEFO, 'exchangeInstrumentID': 39523},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 2885}
               ]

historical_ltp_values = []


NO_POSITION = 0
LONG_POSITION = 1
SHORT_POSITION = -1

class MovingAverageCrossoverStrategy:
    def __init__(self, short_ma_period=2, long_ma_period=4):
        self.short_ma_period = short_ma_period
        self.long_ma_period = long_ma_period
        self.inTransaction=False
        self.position = NO_POSITION
        self.previous_position = NO_POSITION

    def calculate_moving_averages(self, data):
        short_ma = np.mean(data[-self.short_ma_period:])
        long_ma = np.mean(data[-self.long_ma_period:])
        return short_ma, long_ma
    
    def execute_trades(self,short_ma, long_ma):
    # Check for crossover
        if short_ma > long_ma:
            # Bullish crossover
            if self.previous_position == LONG_POSITION:
                print("Already in long position.")
            elif self.previous_position != LONG_POSITION:
                # If not in long position, buy and close short position
                print("Bullish crossover detected! Buying ATM Call Option and closing short position.")
                # Execute buy call and close short put options
                # Function required
                if self.position & self.previous_position == NO_POSITION:
                   self.position = LONG_POSITION
                else:
                    self.previous_position=self.position
                    self.position=LONG_POSITION   

        elif short_ma < long_ma:
            # Bearish crossover
            if self.previous_position == LONG_POSITION:
                print("Already in long position.")
            elif self.previous_position != SHORT_POSITION:
                # If not in short position, buy put and close long position
                print("Bearish crossover detected! Buying ATM Put Option and closing long position.")
                # Execute buy put and close long call options
                if self.position & self.previous_position == NO_POSITION:
                   self.position = SHORT_POSITION
                else:
                    self.previous_position=self.position
                    self.position=SHORT_POSITION  
        else:
            # No crossover
            print("No crossover detected")



# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

    # # Subscribe to instruments
    print('Sending subscription request for Instruments - \n' + str(Instruments))
    response = xtm.send_subscription(Instruments, 1512)
    print('Sent Subscription request!')
    print("Subscription response: ", response)

# Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    return
    print('I received a 1501 Touchline message!' + data)

# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1507 FULL
def on_message1507_json_full(data):
    return
    print('I received a 1507 MarketStatus data message!' + data)

# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    return
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 FULL
def on_message1512_json_full(data):
    data_object=json.loads(data)
    ltp=data_object['LastTradedPrice']
    #print('I received a 1512 Candle data message! in my place',ltp)
    historical_ltp_values.append(ltp)
    short_ma, long_ma = strategy.calculate_moving_averages(historical_ltp_values)
    strategy.execute_trades(short_ma, long_ma)
    print(f"Current Price: {ltp}, Short MA: {short_ma}, Long MA: {long_ma}, Signal: {strategy.position}")

# Callback for message code 1105 FULL
def on_message1105_json_full(data):
    return
    print('I received a 1105, Instrument Property Change Event message!' + data)


# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    return
    print('I received a 1501, Touchline Event message!' + data)

# Callback for message code 1502 PARTIAL
def on_message1502_json_partial(data):
    return
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 PARTIAL
def on_message1505_json_partial(data):
    return
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1510 PARTIAL
def on_message1510_json_partial(data):
    return
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 PARTIAL
def on_message1512_json_partial(data):
    return
    print('I received a 1512, LTP Event message!' + data)



# Callback for message code 1105 PARTIAL
def on_message1105_json_partial(data):
    return
    print('I received a 1105, Instrument Property Change Event message!' + data)

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
soc.on_message1505_json_full = on_message1505_json_full
soc.on_message1507_json_full = on_message1507_json_full
soc.on_message1510_json_full = on_message1510_json_full
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1512_json_full = on_message1512_json_full
soc.on_message1105_json_full = on_message1105_json_full
soc.on_message1502_json_partial = on_message1502_json_partial
soc.on_message1505_json_partial = on_message1505_json_partial
soc.on_message1510_json_partial = on_message1510_json_partial
soc.on_message1501_json_partial = on_message1501_json_partial
soc.on_message1512_json_partial = on_message1512_json_partial
soc.on_message1105_json_partial = on_message1105_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error


# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)
el.on('1507-json-full', on_message1507_json_full)
el.on('1512-json-full', on_message1512_json_full)
el.on('1105-json-full', on_message1105_json_full)


# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)
el.on('1507-json-full', on_message1507_json_full)
el.on('1512-json-full', on_message1512_json_full)
el.on('1105-json-full', on_message1105_json_full)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
strategy = MovingAverageCrossoverStrategy()
soc.connect()

#while True:
#  random_integer = random.randint(0, 100)
#  on_message1512_json_full(random_integer)
#  time.sleep(5)


