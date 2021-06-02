import configparser
import os

import socketio


class OrderSocket_io(socketio.Client):
    """A Socket.IO client.
    This class implements a fully compliant Socket.IO web client with support
    for websocket and long-polling transports.
    :param reconnection: 'True'. if the client should automatically attempt to
                         reconnect to the server after an interruption, or
                         'False' to not reconnect. The default is 'True'.
    :param reconnection_attempts: How many reconnection attempts to issue
                                  before giving up, or 0 for infinity attempts.
                                  The default is 0.
    :param reconnection_delay: How long to wait in seconds before the first
                               reconnection attempt. Each successive attempt
                               doubles this delay.
    :param reconnection_delay_max: The maximum delay between reconnection
                                   attempts.
    :param randomization_factor: Randomization amount for each delay between
                                 reconnection attempts. The default is 0.5,
                                 which means that each delay is randomly
                                 adjusted by +/- 50%.
    :param logger: To enable logging set to 'True' or pass a logger object to
                   use. To disable logging set to 'False'. The default is
                   'False'.
    :param binary: 'True' to support binary payloads, 'False' to treat all
                   payloads as text. On Python 2, if this is set to 'True',
                   'unicode' values are treated as text, and 'str' and
                   'bytes' values are treated as binary.  This option has no
                   effect on Python 3, where text and binary payloads are
                   always automatically discovered.
    :param json: An alternative json module to use for encoding and decoding
                 packets. Custom json modules must have 'dumps' and 'loads'
                 functions that are compatible with the standard library
                 versions.
    """

    def __init__(self, token, userID, reconnection=True, reconnection_attempts=0, reconnection_delay=1,
                 reconnection_delay_max=50000, randomization_factor=0.5, logger=False, binary=False, json=None,
                 **kwargs):
        self.sid = socketio.Client(logger=True, engineio_logger=True)
        self.eventlistener = self.sid
        self.sid.on('connect', self.on_connect)
        self.sid.on('message', self.on_message)
        self.sid.on('joined', self.on_joined)
        self.sid.on('error', self.on_error)
        self.sid.on('order', self.on_order)
        self.sid.on('trade', self.on_trade)
        self.sid.on('position', self.on_position)
        self.sid.on('tradeConversion', self.on_tradeconversion)
        self.sid.on('logout', self.on_messagelogout)
        self.sid.on('disconnect', self.on_disconnect)

        self.userID = userID
        self.token = token

        """Get root url from config file"""
        currDirMain = os.getcwd()
        configParser = configparser.RawConfigParser()
        configFilePath = os.path.join(currDirMain, 'config.ini')
        configParser.read(configFilePath)
        self.port = configParser.get('root_url', 'root').strip()

        port = f'{self.port}/?token='

        self.connection_url = port + self.token + '&userID=' + self.userID + "&apiType=INTERACTIVE"

    def connect(self, headers={}, transports='websocket', namespaces=None, socketio_path='/interactive/socket.io',
                verify=False):
        """Connect to a Socket.IO server.
        :param url: The URL of the Socket.IO server. It can include custom
                    query string parameters if required by the server.
        :param headers: A dictionary with custom headers to send with the
                        connection request.
        :param transports: The list of allowed transports. Valid transports
                           are 'polling' and 'websocket'. If not
                           given, the polling transport is connected first,
                           then an upgrade to websocket is attempted.
        :param namespaces: The list of custom namespaces to connect, in
                           addition to the default namespace. If not given,
                           the namespace list is obtained from the registered
                           event handlers.
        :param socketio_path: The endpoint where the Socket.IO server is
                              installed. The default value is appropriate for
                              most cases.

        """
        """Connect to the socket."""
        url = self.connection_url

        """Connected to the socket."""
        self.sid.connect(url, headers, transports, namespaces, socketio_path)
        self.sid.wait()
        """Disconnect from the socket."""
        # self.sid.disconnect()

    def on_connect(self):
        """Connect from the socket"""
        print('Interactive socket connected successfully!')

    def on_message(self):
        """On message from socket"""
        print('I received a message!')

    def on_joined(self, data):
        """On socket joined"""
        print('Interactive socket joined successfully!' + data)

    def on_error(self, data):
        """On receiving error from socket"""
        print('Interactive socket error!' + data)

    def on_order(self, data):
        """On receiving order placed data from socket"""
        print("Order placed!" + data)

    def on_trade(self, data):
        """On receiving trade data from socket"""
        print("Trade Received!" + data)

    def on_position(self, data):
        """On receiving position data from socket"""
        print("Position Retrieved!" + data)

    def on_tradeconversion(self, data):
        """On receiving trade conversion data from socket"""
        print("Trade Conversion Received!" + data)

    def on_messagelogout(self, data):
        """On receiving user logout message"""
        print("User logged out!" + data)

    def on_disconnect(self):
        """On receiving disconnection from socket"""
        print('Interactive Socket disconnected!')

    def get_emitter(self):
        """For getting event listener"""
        return self.eventlistener
