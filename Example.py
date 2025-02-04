# from XTConnect import XTSConnect
from Connect import XTSConnect


# ----------------------------------------------------------------------------------------------------------------------
# Interactive
# ----------------------------------------------------------------------------------------------------------------------

# Interactive API Credentials
# API_KEY = "YOUR_API_KEY_HERE"
# API_SECRET = "YOUR_API_SECRET_HERE"
# clientID = "YOUR_CLIENT_ID_HERE"
# userID = "YOUR_USER_ID_HERE"
# XTS_API_BASE_URL = "https://xts-api.trading"
# source = "WEBAPI"

"Note : For dealer credentials add the clientID and for investor client leave the clientID blank"

"""Dealer credentials"""
API_KEY = "096328d98d30f4c551c503"
API_SECRET = "Letp625#gV"
clientID = "ATHARVA1"
userID = ""
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Investor client credentials"""
# API_KEY = "431c75e076e238bdff8176"
# API_SECRET = "Ieil074#FH"
# clientID = "RUCHA"
# XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
# source = "WEBAPI"

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the xt object we created call the interactive login Request"""
response = xt.interactive_login()
print("Login: ", response)


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
    apiOrderSource="",
    orderUniqueIdentifier="454845",
    clientID=clientID)

print("Place Order: ", response)


clientID = "ATHARVA1"
"""Order book Request"""
response = xt.get_order_book(clientID)
print("Order Book: ", response)

# extracting the order id from response
if response['type'] != 'error':
    OrderID = response['result']['AppOrderID']

    """Get Order History Request"""
    response = xt.get_order_history(appOrderID=OrderID,clientID=clientID)
    print("Order History: ", response)

    """Modify Order Request"""
    response = xt.modify_order(
        appOrderID=OrderID,
        modifiedProductType=xt.PRODUCT_NRML,
        modifiedOrderType=xt.ORDER_TYPE_LIMIT,
        modifiedOrderQuantity=8,
        modifiedDisclosedQuantity=0,
        modifiedLimitPrice=1405,
        modifiedStopPrice=0,
        modifiedTimeInForce=xt.VALIDITY_DAY,
        orderUniqueIdentifier="454845",
        clientID=clientID
    )
    print("Modify Order: ", response)

    """Cancel Orders Request"""
    response = xt.cancel_order(
        appOrderID=OrderID,
        orderUniqueIdentifier='454845',
        clientID=clientID)
    print("Cancel Order: ", response)

    """Get Order History Request"""
    response = xt.get_order_history(appOrderID=OrderID,clientID=clientID)
    print("Order History: ", response)


"""Place BracketOrder Request"""
response = xt.place_bracketorder(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    orderType=xt.ORDER_TYPE_MARKET,
    orderSide=xt.TRANSACTION_TYPE_BUY,
    disclosedQuantity=0,
    orderQuantity=10,
    limitPrice=59,
    squarOff=1,
    stopLossPrice=1,
	trailingStoploss=1,
    isProOrder=False,
    apiOrderSource="",
    orderUniqueIdentifier="454845"
    )
print("Bracket Order: ", response)

# extracting the order id from response
if response['type'] != 'error':
    OrderID = response['result']['AppOrderID']
    
    """Cancel BracketOrder Request"""
    res = xt.bracketorder_cancel(OrderID)
    print("Bracket Cancel: ", response)

    """Modify BracketOrder Request"""
    response = xt.modify_order(
        appOrderID=OrderID,
        orderQuantity=8,
        limitPrice=1405,
        stopPrice=0,
        clientID=clientID
    )
    print("Modify BracketOrder: ", response)

    
"""Get Profile Request"""
response = xt.get_profile(clientID=userID)
print("Profile: ", response)

"""Get Balance Request"""
response = xt.get_balance(clientID=clientID)
print("Balance: ", response)

"""Get Trade Book Request"""
response = xt.get_trade(clientID=clientID)
print("Trade Book: ", response)

"""Get Holdings Request"""
response = xt.get_holding(clientID=clientID)
print("Holdings: ", response)

"""Get Position by DAY Request"""
response = xt.get_position_daywise(clientID=clientID)
print("Position by Day: ", response)

"""Get Position by NET Request"""
response = xt.get_position_netwise(clientID=clientID)
print("Position by Net: ", response)

"""Get Dealer Position by NET Request"""
response = xt.get_dealerposition_daywise(clientID=clientID)
print("Dealer Position by Net: ", response)

"""Get Dealer Position by DAY Request"""
response = xt.get_dealerposition_netwise(clientID=clientID)
print("Dealer Position by Day: ", response)


"""Dealer Order book Request"""
response = xt.get_dealer_orderbook(clientID)
print("Dealer Order Book: ", response)

"""Get Dealer Trade Book Request"""
response = xt.get_dealer_tradebook(clientID=clientID)
print("Dealer Trade Book: ", response)

"""Position Convert Request"""
response = xt.convert_position(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    targetQty=10,
    isDayWise=True,
    oldProductType=xt.PRODUCT_MIS,
    newProductType=xt.PRODUCT_NRML,
    clientID=clientID)
print("Position Convert: ", response)

"""Place Cover Order Request"""
response = xt.place_cover_order(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    orderSide=xt.TRANSACTION_TYPE_BUY,
    orderType=xt.ORDER_TYPE_LIMIT,
    orderQuantity=2,
    disclosedQuantity=0,
    limitPrice=1802,
    stopPrice=1899,
    apiOrderSource="",
    orderUniqueIdentifier="454845",
    clientID=clientID)
print("Cover Order:", response)

# extracting the order id from response
if response['type'] != 'error':
    OrderID = response['result']['ExitAppOrderID']

    """Exit Cover Order Request"""
    response = xt.exit_cover_order(appOrderID=OrderID, clientID=clientID)
    print("Exit Cover Order:", response)

"""Cancel all Orders Request"""
response = xt.cancelall_order(exchangeInstrumentID=22,exchangeSegment=xt.EXCHANGE_NSECM)
print("Cancel all Orders: ", response)

"""Interactive logout Request"""
response = xt.interactive_logout(clientID=clientID)
print("Interactive Logout: ", response)

exit()

# ----------------------------------------------------------------------------------------------------------------------
# Marketdata
# ----------------------------------------------------------------------------------------------------------------------

# Marketdata API Credentials
API_KEY = "YOUR_API_KEY_HERE"
API_SECRET = "YOUR_API_SECRET_HERE"
XTS_API_BASE_URL = "https://xts-api.trading"
source = "WEBAPI"

"""Dealer login credentials"""
API_KEY = "22f6f9dad2fe3982419756"
API_SECRET = "Bxtj027$Dr"
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Investor client login credentials"""
API_KEY = "76179cbae91810ddda7774"
API_SECRET = "Bylg203#fv"
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the object we call the login function Request"""
response = xt.marketdata_login()
print("MarketData Login: ", response)

"""Get Config Request"""
response = xt.get_config()
print('Config :', response)

"""instruments list"""
instruments = [
    {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

"""Get Quote Request"""
response = xt.get_quote(
    Instruments=instruments,
    xtsMessageCode=1502,
    publishFormat='JSON')
print('Quote :', response)

"""Send Subscription Request"""
response = xt.send_subscription(
    Instruments=instruments,
    xtsMessageCode=1502)
print('Subscribe :', response)

"""Send Unsubscription Request"""
response = xt.send_unsubscription(
    Instruments=instruments,
    xtsMessageCode=1502)
print('Unsubscribe :', response)

"""Get Master Instruments Request"""
exchangesegments = [xt.EXCHANGE_NSECM, xt.EXCHANGE_NSEFO]
response = xt.get_master(exchangeSegmentList=exchangesegments)
print("Master: " + str(response))

"""Get OHLC Request"""
response = xt.get_ohlc(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=22,
    startTime='Jan 04 2025 090000',
    endTime='Jan 04 2019 150000',
    compressionValue='60')
print("OHLC: " + str(response))

"""Get Series Request"""
response = xt.get_series(exchangeSegment=1)
print('Series:', str(response))

"""Get Equity Symbol Request"""
response = xt.get_equity_symbol(
    exchangeSegment=1,
    series='EQ',
    symbol='Acc')
print('Equity Symbol:', str(response))

"""Get Expiry Date Request"""
response = xt.get_expiry_date(
    exchangeSegment=2,
    series='FUTIDX',
    symbol='NIFTY')
print('Expiry Date:', str(response))

"""Get Future Symbol Request"""
response = xt.get_future_symbol(
    exchangeSegment=2,
    series='FUTIDX',
    symbol='NIFTY',
    expiryDate='28MAY25JUN')
print('Future Symbol:', str(response))

"""Get Option Symbol Request"""
response = xt.get_option_symbol(
    exchangeSegment=2,
    series='OPTIDX',
    symbol='NIFTY',
    expiryDate='26Mar2020',
    optionType='CE',
    strikePrice=10000)
print('Option Symbol:', str(response))

"""Get Option Type Request"""
response = xt.get_option_type(
    exchangeSegment=2,
    series='OPTIDX',
    symbol='NIFTY',
    expiryDate='26Mar2020')
print('Option Type:', str(response))

"""Get Index List Request"""
response = xt.get_index_list(exchangeSegment=xt.EXCHANGE_NSECM)
print('Index List:', str(response))

"""Search Instrument by ID Request"""
response = xt.search_by_instrumentid(Instruments=instruments)
print('Search By Instrument ID:', str(response))

"""Search Instrument by Scriptname Request"""
response = xt.search_by_scriptname(searchString='REL')
print('Search By Symbol :', str(response))

"""Marketdata Logout Request"""
response = xt.marketdata_logout()
print('Marketdata Logout :', str(response))
