#!/usr/bin/env python3

from bottle import template

def frontpage():
    return template("frontpage")

def cow():
    return template("cow")

@route('views/header')
def header():
    return template("header")

def krmckelv():
    return template("krmckelv")
