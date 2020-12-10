from XTConnect import XTSConnect

# logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# Interactive
# ----------------------------------------------------------------------------------------------------------------------

# Interactive API Credentials
# API_KEY = "YOUR_API_KEY_HERE"
# API_SECRET = "YOUR_API_SECRET_HERE"
# XTS_API_BASE_URL = "https://xts-api.trading"
# source = "WEBAPI"

API_KEY = "15fc93db915525ec829191"
API_SECRET = "Jwfr052#RY"
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the xt object we created call the interactive login Request"""
response = xt.interactive_login()
print("Login: ", response)

"""Order book Request"""
response = xt.get_order_book()
print("Order Book: ", response)

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
print("Place Order: ", response)


# extracting the order id from response
if response['type'] != 'error':
    OrderID = response['result']['AppOrderID']

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
        orderUniqueIdentifier="454845"
    )
    print("Modify Order: ", response)

    """Cancel Orders Request"""
    response = xt.cancel_order(
        appOrderID=OrderID,
        orderUniqueIdentifier='454845')
    print("Cancel Order: ", response)

    """Get Order History Request"""
    response = xt.get_order_history(appOrderID=OrderID)
    print("Order History: ", response)

"""Get Profile Request"""
response = xt.get_profile()
print("Profile: ", response)

"""Get Balance Request"""
response = xt.get_balance()
print("Balance: ", response)

"""Get Trade Book Request"""
response = xt.get_trade()
print("Trade Book: ", response)

"""Get Holdings Request"""
response = xt.get_holding()
print("Holdings: ", response)

"""Get Position by DAY Request"""
response = xt.get_position_daywise()
print("Position by Day: ", response)

"""Get Position by NET Request"""
response = xt.get_position_netwise()
print("Position by Net: ", response)

"""Position Convert Request"""
response = xt.convert_position(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    targetQty=10,
    isDayWise=True,
    oldProductType=xt.PRODUCT_MIS,
    newProductType=xt.PRODUCT_NRML)
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
    orderUniqueIdentifier="454845")
print("Cover Order:", response)

# extracting the order id from response
if response['type'] != 'error':
    OrderID = response['result']['ExitAppOrderID']

    """Exit Cover Order Request"""
    response = xt.exit_cover_order(appOrderID=OrderID)
    print("Exit Cover Order:", response)

"""Position Squareoff Request"""
response = xt.squareoff_position(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=2885,
    productType=xt.PRODUCT_MIS,
    squareoffMode=xt.SQUAREOFF_DAYWISE,
    positionSquareOffQuantityType=xt.SQUAREOFFQUANTITY_EXACTQUANTITY,
    squareOffQtyValue=5,
    blockOrderSending=True,
    cancelOrders=True)
print("Position Squareoff: ", response)

"""Interactive logout Request"""
response = xt.interactive_logout()
print("Interactive Logout: ", response)

# ----------------------------------------------------------------------------------------------------------------------
# Marketdata
# ----------------------------------------------------------------------------------------------------------------------

# Marketdata API Credentials
# API_KEY = "YOUR_API_KEY_HERE"
# API_SECRET = "YOUR_API_SECRET_HERE"
# XTS_API_BASE_URL = "https://xts-api.trading"
# source = "WEBAPI"

API_KEY = "c2368d9aabcafe7a3e8529"
API_SECRET = "Xogi551#V5"
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
    xtsMessageCode=1504,
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
    startTime='Dec 16 2019 090000',
    endTime='Dec 18 2019 150000',
    compressionValue=1)
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
