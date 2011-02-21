#!/usr/bin/env python3

from bottle import route
from bottle import static_file

"""
This module handles all of the URL dispatching for Guido, mapping from URLs to
the functions that will be called in response.
"""

import frontpage

@route('/')
def index():
    return frontpage.frontpage()

@route('/cow')
def meet_mr_cow():
    return frontpage.cow()

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')
