#!/usr/bin/env python3

from bottle import template

def frontpage():
    return template("frontpage")

def cow():
    return template("cow")

def pig():
    return template("pig")
