#!/usr/bin/env python3

from bottle import template
from bottle import route

def frontpage():
    return template("frontpage")

def assignment_notes():
    return template("assignment_notes")

def startpage():
    return template("startpage")
