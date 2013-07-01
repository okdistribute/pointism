#!/usr/bin/env python3

from bottle import template
from bottle import redirect

import model
import queries

THEDB = "guidodb"

def choice():
    return template("edit_database")

def choose(choicetype):
    if(choicetype == 'comments'):
        return comments()
    else:
        return template("unsupported")

def comments():
    redirect('/edit_database_comments')

def assignments():
    return template("unsupported")

def students():
    return template("unsupported")
