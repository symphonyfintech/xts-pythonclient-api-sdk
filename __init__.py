# -*- coding: utf-8 -*-
"""
XTS Connect API client for Python.

Symphony Fintech Pvt. Ltd.

License
-------
XTSConnect Python library is licensed.

The library
-----------
XTS Connect is a set of RESTful APIs that expose
many capabilities required to build a complete
investment and trading platform. Execute orders in
real time, manage user portfolio, stream live market
data (WebSockets), and more, with the simple HTTP API collection

This module provides an easy to use abstraction over the HTTP APIs.
The HTTP calls have been converted to methods and their JSON responses
are returned as native Python structures, for example, dicts, lists, bools etc.
See the **[XTS Connect API documentation]**
for the complete list of APIs, supported parameters and values, and response formats.

"""

# from __future__ import unicode_literals, absolute_import

from XTConnect import Exception
from XTConnect.Connect import XTSConnect

__all__ = ["XTConnect", "Exception"]
