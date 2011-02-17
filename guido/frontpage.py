#!/usr/bin/env python3

from bottle import template
from bottle import route

def frontpage():
    return template("frontpage")

@route('/header')
def header():
    return template("header")
