from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import random
import time
import requests

"Note : For dealer credentials add the clientID and for investor client leave the clientID blank"

"""InVestor credentials"""
API_KEYS = ["48fea59dfc71428ba1a335","48fea59dfc71428ba1a335"]
API_SECRETS = ["Atei167#ys","Atei167#ys"]
source = "WEBAPI"

def connect(API,KEY):
        xt = XTSConnect(API, KEY, source)
        """Using the xt object we created call the interactive login Request"""
        response_o = xt.interactive_login()
        #print("Login: ", response_o)
        return response_o

def login(API_KEYS,API_SECRETS):
    with ThreadPoolExecutor() as executor:
        results=executor.map(connect,API_KEYS,API_SECRETS)
        for result in results:
             print(result)
             time.sleep(3)
       
login(API_KEYS,API_SECRETS)    