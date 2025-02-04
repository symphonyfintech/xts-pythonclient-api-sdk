"""
    Connect.py

    API wrapper for XTS Connect REST APIs.

    :copyright:
    :license: see LICENSE for details.
"""
import configparser
import json
import logging
import requests
from urllib import parse
import Exception as ex
log = logging.getLogger(__name__)


class XTSCommon:
    """
    Base variables class
    """

    def __init__(self, token=None, userID=None, isInvestorClient=None):
        """Initialize the common variables."""
        self.token = token
        self.userID = userID
        self.isInvestorClient = isInvestorClient


class XTSConnect(XTSCommon):
    """
    The XTS Connect API wrapper class.
    In production, you may initialise a single instance of this class per `api_key`.
    """
    """Get the configurations from config.ini"""
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    # Default root API endpoint. It's possible to
    # override this by passing the `root` parameter during initialisation.
    _default_root_uri = cfg.get('root_url', 'root')
    _default_login_uri = _default_root_uri + "/user/session"
    _default_timeout = 7  # In seconds

    # SSL Flag
    _ssl_flag = cfg.get('SSL', 'disable_ssl')

    # Constants
    # Products
    PRODUCT_MIS = "MIS"
    PRODUCT_NRML = "NRML"

    # Order types
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_STOPMARKET = "STOPMARKET"
    ORDER_TYPE_STOPLIMIT = "STOPLIMIT"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    # Squareoff mode
    SQUAREOFF_DAYWISE = "DayWise"
    SQUAREOFF_NETWISE = "Netwise"

    # Squareoff position quantity types
    SQUAREOFFQUANTITY_EXACTQUANTITY = "ExactQty"
    SQUAREOFFQUANTITY_PERCENTAGE = "Percentage"

    # Validity
    VALIDITY_DAY = "DAY"

    # Exchange Segments
    EXCHANGE_NSECM = "NSECM"
    EXCHANGE_NSEFO = "NSEFO"
    EXCHANGE_NSECD = "NSECD"
    EXCHANGE_MCXFO = "MCXFO"
    EXCHANGE_BSECM = "BSECM"
    EXCHANGE_BSEFO = "BSEFO"

    # URIs to various calls
    _routes = {
        # Interactive API endpoints
        "interactive.prefix": "interactive",
        "user.login": "/interactive/user/session",
        "user.logout": "/interactive/user/session",
        "user.profile": "/interactive/user/profile",
        "user.balance": "/interactive/user/balance",

        "orders": "/interactive/orders",
        "trades": "/interactive/orders/trades",
        "order.status": "/interactive/orders",
        "order.place": "/interactive/orders",
        "bracketorder.place": "/interactive/orders/bracket",
	    "bracketorder.modify": "/interactive/orders/bracket",
        "bracketorder.cancel": "/interactive/orders/bracket",
        "order.place.cover": "/interactive/orders/cover",
        "order.exit.cover": "/interactive/orders/cover",
        "order.modify": "/interactive/orders",
        "order.cancel": "/interactive/orders",
        "order.cancelall": "/interactive/orders/cancelall",
        "order.history": "/interactive/orders",

        "portfolio.positions": "/interactive/portfolio/positions",
        "portfolio.holdings": "/interactive/portfolio/holdings",
        "portfolio.positions.convert": "/interactive/portfolio/positions/convert",
        "portfolio.squareoff": "/interactive/portfolio/squareoff",
        "portfolio.dealerpositions": "interactive/portfolio/dealerpositions",
        "order.dealer.status": "/interactive/orders/dealerorderbook",
        "dealer.trades": "/interactive/orders/dealertradebook",




        # Market API endpoints
        "marketdata.prefix": "apimarketdata",
        "market.login": "/apimarketdata/auth/login",
        "market.logout": "/apimarketdata/auth/logout",

        "market.config": "/apimarketdata/config/clientConfig",

        "market.instruments.master": "/apimarketdata/instruments/master",
        "market.instruments.subscription": "/apimarketdata/instruments/subscription",
        "market.instruments.unsubscription": "/apimarketdata/instruments/subscription",
        "market.instruments.ohlc": "/apimarketdata/instruments/ohlc",
        "market.instruments.indexlist": "/apimarketdata/instruments/indexlist",
        "market.instruments.quotes": "/apimarketdata/instruments/quotes",

        "market.search.instrumentsbyid": '/apimarketdata/search/instrumentsbyid',
        "market.search.instrumentsbystring": '/apimarketdata/search/instruments',

        "market.instruments.instrument.series": "/apimarketdata/instruments/instrument/series",
        "market.instruments.instrument.equitysymbol": "/apimarketdata/instruments/instrument/symbol",
        "market.instruments.instrument.futuresymbol": "/apimarketdata/instruments/instrument/futureSymbol",
        "market.instruments.instrument.optionsymbol": "/apimarketdata/instruments/instrument/optionsymbol",
        "market.instruments.instrument.optiontype": "/apimarketdata/instruments/instrument/optionType",
        "market.instruments.instrument.expirydate": "/apimarketdata/instruments/instrument/expiryDate"
    }

    def __init__(self,
                 apiKey,
                 secretKey,
                 source,
                 root=None,
                 debug=False,
                 timeout=None,
                 pool=None,
                 disable_ssl=_ssl_flag):
        """
        Initialise a new XTS Connect client instance.

        - `api_key` is the key issued to you
        - `token` is the token obtained after the login flow. Pre-login, this will default to None,
        but once you have obtained it, you should persist it in a database or session to pass
        to the XTS Connect class initialisation for subsequent requests.
        - `root` is the API end point root. Unless you explicitly
        want to send API requests to a non-default endpoint, this
        can be ignored.
        - `debug`, if set to True, will serialise and print requests
        and responses to stdout.
        - `timeout` is the time (seconds) for which the API client will wait for
        a request to complete before it fails. Defaults to 7 seconds
        - `pool` is manages request pools. It takes a dict of params accepted by HTTPAdapter
        - `disable_ssl` disables the SSL verification while making a request.
        If set requests won't throw SSLError if its set to custom `root` url without SSL.
        """
        self.debug = debug
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.source = source
        self.disable_ssl = disable_ssl
        self.root = root or self._default_root_uri
        self.timeout = timeout or self._default_timeout

        super().__init__()

        # Create requests session only if pool exists. Reuse session
        # for every request. Otherwise create session for each request
        if pool:
            self.reqsession = requests.Session()
            reqadapter = requests.adapters.HTTPAdapter(**pool)
            self.reqsession.mount("https://", reqadapter)
        else:
            self.reqsession = requests

        # disable requests SSL warning
        requests.packages.urllib3.disable_warnings()

    def _set_common_variables(self, access_token,userID, isInvestorClient):
        """Set the `access_token` received after a successful authentication."""
        super().__init__(access_token,userID, isInvestorClient)

    def _login_url(self):
        """Get the remote login url to which a user should be redirected to initiate the login flow."""
        return self._default_login_uri

    def interactive_login(self):
        """Send the login url to which a user should receive the token."""
        try:
            params = {
                "appKey": self.apiKey,
                "secretKey": self.secretKey,
                "source": self.source
            }
            response = self._post("user.login", params)

            if "token" in response['result']:
                self._set_common_variables(response['result']['token'], response['result']['userID'],
                                           response['result']['isInvestorClient'])
            return response
        except Exception as e:
            return response['description']

    def get_order_book(self, clientID=None):
        """Request Order book gives states of all the orders placed by an user"""
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get("order.status", params)
            return response
        except Exception as e:
            return response['description']
		
    def get_dealer_orderbook(self, clientID=None):
        """Request Order book gives states of all the orders placed by an user"""
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get("order.dealer.status", params)
            return response
        except Exception as e:
            return response['description']


    def place_order(self,
                    exchangeSegment,
                    exchangeInstrumentID,
                    productType,
                    orderType,
                    orderSide,
                    timeInForce,
                    disclosedQuantity,
                    orderQuantity,
                    limitPrice,
                    stopPrice,
                    orderUniqueIdentifier,
                    apiOrderSource,
                    clientID=None
                    ):
        """To place an order"""
        try:

            params = {
                "exchangeSegment": exchangeSegment,
                "exchangeInstrumentID": exchangeInstrumentID,
                "productType": productType,
                "orderType": orderType,
                "orderSide": orderSide,
                "timeInForce": timeInForce,
                "disclosedQuantity": disclosedQuantity,
                "orderQuantity": orderQuantity,
                "limitPrice": limitPrice,
                "stopPrice": stopPrice,
                "apiOrderSource":apiOrderSource,
                "orderUniqueIdentifier": orderUniqueIdentifier
            }

            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._post('order.place', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def modify_order(self,
                     appOrderID,
                     modifiedProductType,
                     modifiedOrderType,
                     modifiedOrderQuantity,
                     modifiedDisclosedQuantity,
                     modifiedLimitPrice,
                     modifiedStopPrice,
                     modifiedTimeInForce,
                     orderUniqueIdentifier,
                     clientID=None
                     ):
        """The facility to modify your open orders by allowing you to change limit order to market or vice versa,
        change Price or Quantity of the limit open order, change disclosed quantity or stop-loss of any
        open stop loss order. """
        try:
            appOrderID = int(appOrderID)
            params = {
                'appOrderID': appOrderID,
                'modifiedProductType': modifiedProductType,
                'modifiedOrderType': modifiedOrderType,
                'modifiedOrderQuantity': modifiedOrderQuantity,
                'modifiedDisclosedQuantity': modifiedDisclosedQuantity,
                'modifiedLimitPrice': modifiedLimitPrice,
                'modifiedStopPrice': modifiedStopPrice,
                'modifiedTimeInForce': modifiedTimeInForce,
                'orderUniqueIdentifier': orderUniqueIdentifier
            }

            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._put('order.modify', json.dumps(params))
            return response
        except Exception as e:
            return response['description']


        
    def place_bracketorder(self,
                    exchangeSegment,
                    exchangeInstrumentID,
                    orderType,
                    orderSide,
                    disclosedQuantity,
                    orderQuantity,
                    limitPrice,
                    squarOff,
                    stopLossPrice,
	                trailingStoploss,
                    isProOrder,
                    apiOrderSource,
                    orderUniqueIdentifier,
                     ):
        """To place a bracketorder"""
        try:

            params = {
                "exchangeSegment": exchangeSegment,
                "exchangeInstrumentID": exchangeInstrumentID,
                "orderType": orderType,
                "orderSide": orderSide,
                "disclosedQuantity": disclosedQuantity,
                "orderQuantity": orderQuantity,
                "limitPrice": limitPrice,
                "squarOff": squarOff,
                "stopLossPrice": stopLossPrice,
                "trailingStoploss": trailingStoploss,
                "isProOrder": isProOrder,
                "apiOrderSource":apiOrderSource,
                "orderUniqueIdentifier": orderUniqueIdentifier
            }
            response = self._post('bracketorder.place', json.dumps(params))
            print(response)
            return response
        except Exception as e:
            return response['description']

    def bracketorder_cancel(self, appOrderID, clientID=None):
        """This API can be called to cancel any open order of the user by providing correct appOrderID matching with
        the chosen open order to cancel. """
        try:
            params = {'boEntryOrderId': int(appOrderID)}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._delete('bracketorder.cancel', params)
            return response
        except Exception as e:
            return response['description']   

    def modify_bracketorder(self,
                     appOrderID,
                     orderQuantity,
                     limitPrice,
                     stopPrice,
                     clientID=None
                     ):
        try:
            appOrderID = int(appOrderID)
            params = {
                'appOrderID': appOrderID,
                'bracketorder.modify': orderQuantity,
                'limitPrice': limitPrice,
                'stopPrice': stopPrice
            }

            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._put('bracketorder.modify', json.dumps(params))
            return response
        except Exception as e:
            return response['description']


    def place_cover_order(self, 
                          exchangeSegment, 
                          exchangeInstrumentID, 
                          orderSide,orderType, 
                          orderQuantity, 
                          disclosedQuantity,
                          limitPrice, 
                          stopPrice, 
                          apiOrderSource,
                          orderUniqueIdentifier, 
                          clientID=None):
        """A Cover Order is an advance intraday order that is accompanied by a compulsory Stop Loss Order. This helps
        users to minimize their losses by safeguarding themselves from unexpected market movements. A Cover Order
        offers high leverage and is available in Equity Cash, Equity F&O, Commodity F&O and Currency F&O segments. It
        has 2 orders embedded in itself, they are Limit/Market Order Stop Loss Order """
        try:

            params = {'exchangeSegment': exchangeSegment, 
                      'exchangeInstrumentID': exchangeInstrumentID,
                      'orderSide': orderSide, 
                      "orderType": orderType,
                      'orderQuantity': orderQuantity, 
                      'disclosedQuantity': disclosedQuantity,
                      'limitPrice': limitPrice, 
                      'stopPrice': stopPrice, 
                      'apiOrderSource': apiOrderSource,
                      'orderUniqueIdentifier': orderUniqueIdentifier
                      }
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._post('order.place.cover', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def exit_cover_order(self, appOrderID, clientID=None):
        """Exit Cover API is a functionality to enable user to easily exit an open stoploss order by converting it
        into Exit order. """
        try:

            params = {'appOrderID': appOrderID}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._put('order.exit.cover', json.dumps(params))
            return response
        except Exception as e:
            return response['description']



    def get_profile(self, clientID=None):
        """Using session token user can access his profile stored with the broker, it's possible to retrieve it any
        point of time with the http: //ip:port/interactive/user/profile API. """
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._get('user.profile', params)
            return response
        except Exception as e:
            return response['description']

    def get_balance(self, clientID=None):
        """Get Balance API call grouped under this category information related to limits on equities, derivative,
        upfront margin, available exposure and other RMS related balances available to the user."""
        if self.isInvestorClient:
            try:
                params = {}
                if not self.isInvestorClient:
                    params['clientID'] = clientID
                response = self._get('user.balance', params)
                return response
            except Exception as e:
                return response['description']
        else:
            print("Balance : Balance API available for retail API users only, dealers can watch the same on dealer "
                  "terminal")


    def get_trade(self, clientID=None):
        """Trade book returns a list of all trades executed on a particular day , that were placed by the user . The
        trade book will display all filled and partially filled orders. """
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get('trades', params)
            return response
        except Exception as e:
            return response['description']

    def get_dealer_tradebook(self, clientID=None):
        """Trade book returns a list of all trades executed on a particular day , that were placed by the user . The
        trade book will display all filled and partially filled orders. """
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get('dealer.trades', params)
            return response
        except Exception as e:
            return response['description']
		
    def get_holding(self, clientID=None):
        """Holdings API call enable users to check their long term holdings with the broker."""
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._get('portfolio.holdings', params)
            return response
        except Exception as e:
            return response['description']


    def get_dealerposition_netwise(self, clientID=None):
        """The positions API positions by net. Net is the actual, current net position portfolio."""
        try:
            params = {'dayOrNet': 'NetWise'}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get('portfolio.dealerpositions', params)
            return response
        except Exception as e:
            return response['description']


           
    def get_dealerposition_daywise(self, clientID=None):
        """The positions API returns positions by day, which is a snapshot of the buying and selling activity for
        that particular day."""
        try:
            params = {'dayOrNet': 'DayWise'}
            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._get('portfolio.dealerpositions', params)
            return response
        except Exception as e:
            return response['description']
		
    def get_position_daywise(self, clientID=None):
	    
        """The positions API returns positions by day, which is a snapshot of the buying and selling activity for
        that particular day."""
        try:
            params = {'dayOrNet': 'DayWise'}
            if not self.isInvestorClient:
                params['clientID'] = clientID

            response = self._get('portfolio.positions', params)
            return response
        except Exception as e:
            return response['description']

    def get_position_netwise(self, clientID=None):
        """The positions API positions by net. Net is the actual, current net position portfolio."""
        try:
            params = {'dayOrNet': 'NetWise'}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get('portfolio.positions', params)
            return response
        except Exception as e:
            return response['description']

    def convert_position(self, exchangeSegment, exchangeInstrumentID, targetQty, isDayWise, oldProductType,
                         newProductType, clientID=None):
        """Convert position API, enable users to convert their open positions from NRML intra-day to Short term MIS or
        vice versa, provided that there is sufficient margin or funds in the account to effect such conversion """
        try:
            params = {
                'exchangeSegment': exchangeSegment,
                'exchangeInstrumentID': exchangeInstrumentID,
                'targetQty': targetQty,
                'isDayWise': isDayWise,
                'oldProductType': oldProductType,
                'newProductType': newProductType
            }
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._put('portfolio.positions.convert', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def cancel_order(self, appOrderID, orderUniqueIdentifier, clientID=None):
        """This API can be called to cancel any open order of the user by providing correct appOrderID matching with
        the chosen open order to cancel. """
        try:
            params = {'appOrderID': int(appOrderID), 'orderUniqueIdentifier': orderUniqueIdentifier}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._delete('order.cancel', params)
            return response
        except Exception as e:
            return response['description']
        
    def cancelall_order(self, exchangeSegment, exchangeInstrumentID):
        """This API can be called to cancel all open order of the user by providing exchange segment and exchange instrument ID """
        try:
            params = {"exchangeSegment": exchangeSegment, "exchangeInstrumentID": exchangeInstrumentID}
            if not self.isInvestorClient:
                params['clientID'] = self.userID
            response = self._post('order.cancelall', json.dumps(params))
            return response
        except Exception as e:
            return response['description']    


    def squareoff_position(self, exchangeSegment, exchangeInstrumentID, productType, squareoffMode,
                           positionSquareOffQuantityType, squareOffQtyValue, blockOrderSending, cancelOrders,
                           clientID=None):
        """User can request square off to close all his positions in Equities, Futures and Option. Users are advised
        to use this request with caution if one has short term holdings. """
        try:

            params = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                      'productType': productType, 'squareoffMode': squareoffMode,
                      'positionSquareOffQuantityType': positionSquareOffQuantityType,
                      'squareOffQtyValue': squareOffQtyValue, 'blockOrderSending': blockOrderSending,
                      'cancelOrders': cancelOrders
                      }
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._put('portfolio.squareoff', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def get_order_history(self, appOrderID, clientID=None):
        """Order history will provide particular order trail chain. This indicate the particular order & its state
        changes. i.e.Pending New to New, New to PartiallyFilled, PartiallyFilled, PartiallyFilled & PartiallyFilled
        to Filled etc """
        try:
            params = {'appOrderID': appOrderID}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._get('order.history', params)
            return response
        except Exception as e:
            return response['description']

    def interactive_logout(self, clientID=None):
        """This call invalidates the session token and destroys the API session. After this, the user should go
        through login flow again and extract session token from login response before further activities. """
        try:
            params = {}
            if not self.isInvestorClient:
                params['clientID'] = clientID
            response = self._delete('user.logout', params)
            return response
        except Exception as e:
            return response['description']

########################################################################################################
# Market data API
########################################################################################################

    def marketdata_login(self):
        try:
            params = {
                "appKey": self.apiKey,
                "secretKey": self.secretKey,
                "source": self.source
            }
            response = self._post("market.login", params)

            if "token" in response['result']:
                self._set_common_variables(response['result']['token'], response['result']['userID'],False)
            return response
        except Exception as e:
            return response['description']

    def get_config(self):
        try:
            params = {}
            response = self._get('market.config', params)
            return response
        except Exception as e:
            return response['description']

    def get_quote(self, Instruments, xtsMessageCode, publishFormat):
        try:

            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode, 'publishFormat': publishFormat}
            response = self._post('market.instruments.quotes', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def send_subscription(self, Instruments, xtsMessageCode):
        try:
            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = self._post('market.instruments.subscription', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def send_unsubscription(self, Instruments, xtsMessageCode):
        try:
            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = self._put('market.instruments.unsubscription', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def get_master(self, exchangeSegmentList):
        try:
            params = {"exchangeSegmentList": exchangeSegmentList}
            response = self._post('market.instruments.master', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def get_ohlc(self, exchangeSegment, exchangeInstrumentID, startTime, endTime, compressionValue):
        try:
            params = {
                'exchangeSegment': exchangeSegment,
                'exchangeInstrumentID': exchangeInstrumentID,
                'startTime': startTime,
                'endTime': endTime,
                'compressionValue': compressionValue}
            response = self._get('market.instruments.ohlc', params)
            return response
        except Exception as e:
            return response['description']

    def get_series(self, exchangeSegment):
        try:
            params = {'exchangeSegment': exchangeSegment}
            response = self._get('market.instruments.instrument.series', params)
            return response
        except Exception as e:
            return response['description']

    def get_equity_symbol(self, exchangeSegment, series, symbol):
        try:

            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            response = self._get('market.instruments.instrument.equitysymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_expiry_date(self, exchangeSegment, series, symbol):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            response = self._get('market.instruments.instrument.expirydate', params)
            return response
        except Exception as e:
            return response['description']

    def get_future_symbol(self, exchangeSegment, series, symbol, expiryDate):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            response = self._get('market.instruments.instrument.futuresymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_option_symbol(self, exchangeSegment, series, symbol, expiryDate, optionType, strikePrice):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate,
                      'optionType': optionType, 'strikePrice': strikePrice}
            response = self._get('market.instruments.instrument.optionsymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_option_type(self, exchangeSegment, series, symbol, expiryDate):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            response = self._get('market.instruments.instrument.optiontype', params)
            return response
        except Exception as e:
            return response['description']

    def get_index_list(self, exchangeSegment):
        try:
            params = {'exchangeSegment': exchangeSegment}
            response = self._get('market.instruments.indexlist', params)
            return response
        except Exception as e:
            return response['description']

    def search_by_instrumentid(self, Instruments):
        try:
            params = {'source': self.source, 'instruments': Instruments}
            response = self._post('market.search.instrumentsbyid', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def search_by_scriptname(self, searchString):
        try:
            params = {'searchString': searchString}
            response = self._get('market.search.instrumentsbystring', params)
            return response
        except Exception as e:
            return response['description']

    def marketdata_logout(self):
        try:
            params = {}
            response = self._delete('market.logout', params)
            return response
        except Exception as e:
            return response['description']

    ########################################################################################################
    # Common Methods
    ########################################################################################################

    def _get(self, route, params=None):
        """Alias for sending a GET request."""
        return self._request(route, "GET", params)

    def _post(self, route, params=None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", params)

    def _put(self, route, params=None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", params)

    def _delete(self, route, params=None):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", params)

    def _request(self, route, method, parameters=None):
        """Make an HTTP request."""
        params = parameters if parameters else {}

        # Form a restful URL
        uri = self._routes[route].format(params)
        url = parse.urljoin(self.root, uri)
        headers = {}

        if self.token:
            # set authorization header
            headers.update({'Content-Type': 'application/json', 'Authorization': self.token})

        try:
            r = self.reqsession.request(method,
                                        url,
                                        data=params if method in ["POST", "PUT"] else None,
                                        params=params if method in ["GET", "DELETE"] else None,
                                        headers=headers,
                                        verify=not self.disable_ssl)

        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(code=r.status_code, content=r.content))

        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise ex.XTSDataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=r.content))

            # api error
            if data.get("type"):

                if r.status_code == 400 and data["type"] == "error" and data["description"] == "Invalid Token":
                    raise ex.XTSTokenException(data["description"])

                if r.status_code == 400 and data["type"] == "error" and data["description"] == "Bad Request":
                    message = "Description: " + data["description"] + " errors: " + str(data['result']["errors"])
                    raise ex.XTSInputException(str(message))

            return data
        else:
            raise ex.XTSDataException("Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=r.headers["content-type"],
                content=r.content))
