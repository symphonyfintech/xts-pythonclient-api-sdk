# XTS-SDK-Client Python

This is the XTS Python API Client library , which has both Marketdata and Interactive services.
API Documentation for XTS-MarketData API and XTS-Trading API can be found in the below link.

https://symphonyfintech.com/xts-market-data-front-end-api/

https://symphonyfintech.com/xts-trading-front-end-api-v2/

## Installation

### Prerequisites

    Python 3.8 or above.
    Internet Access.
    
    Execute below command:
    pip install -r requirements.txt

### Usage
Check the config.ini file, need to add the root url keep source as WEBAPI and disable_ssl as true
```
	[user]
	source=WEBAPI

	[SSL]
	disable_ssl=True

	[root_url]
	root=https://developers.symphonyfintech.in
	broadcastMode=Full
```

#### Create XT Connect Object

```js
    """API Credentials"""  
	API_KEY = "YOUR_API_KEY_HERE"
	API_SECRET = "YOUR_API_SECRET_HERE"
	XTS_API_BASE_URL = "https://xts-api.trading"
	source = "WEBAPI"

	"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
	xt = XTSConnect(API_KEY, API_SECRET, source)
```

#### Login
To login into API call the login service which will return a token. This token will help you to access other services throughout the session.
```js
	"""Marketdata Login"""
    response = xt.marketdata_login()
	
	"""Interactive Login"""
	response = xt.interactive_login()
	
```

#### Subscribe
To Subscribe to symbol use marketdata API. It returns Subscribe Response object which will contain the tick data like LTP, Open, High etc
```js
	"""instruments list"""
	instruments = [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},{'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

	"""Send Subscription Request"""
	response = xt.send_subscription(
    Instruments=instruments,
    xtsMessageCode=1502)
```

#### Quotes
Quote service returns Asks, Bids and Touchline
```js
	"""instruments list"""
	instruments = [
		{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
		{'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

	"""Get Quote Request"""
	response = xt.get_quote(
		Instruments=instruments,
		xtsMessageCode=1504,
		publishFormat='JSON')
```
#### PlaceOrder
To Place an order you need to use Interactive API. Response will contain an orderid.
```js
"""Place Order Request"""
response = xt.place_order(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    productType=xt.PRODUCT_MIS,
    orderType=xt.ORDER_TYPE_MARKET,
    orderSide=xt.TRANSACTION_TYPE_BUY,
    timeInForce=xt.VALIDITY_DAY,
    disclosedQuantity=0,
    orderQuantity=10,
    limitPrice=0,
    stopPrice=0,
    orderUniqueIdentifier="454845")
```

#### CancelOrder
To Cancel an order you need to user Interactive api and In response you will get orderid.
```js
  """Cancel Orders Request"""
    response = xt.cancel_order(
        appOrderID=OrderID,
        orderUniqueIdentifier='454845')
 ```
 
 #### Streams and Events
 Events such as TouchLine, MarketData, CandleData, OpenInterest and Index are received from socket.To get those events XTSAPIMarketdataEvents interface needs to be implemented. 
 Event will be received in the respective overridden methods.
 ```js
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
 ```

### Examples
Example code demonstrating how to use XTS Api can be found in xts-python-api-sdk

Example.py : Examples of all the API calls for Interactive as well as Marketdata APIs

InteractiveSocketExample.py : Interactive Socket Streaming Example

MarketdataSocketExample.py : Marketdata Socket Streaming Example

