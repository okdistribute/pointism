#!/usr/bin/env python3

from bottle import route
from bottle import static_file
from bottle import request
import sqlite3

"""
This module handles all of the URL dispatching for Guido, mapping from URLs to
the functions that will be called in response.
"""

import grading
import frontpage
import assignment_notes
import sqlite3

THEDB = 'guidodb'

@route('/')
def index():
    return frontpage.frontpage()

@route('/cow')
def meet_mr_cow():
    return frontpage.cow()

@route('/pig')
def see_pig():
    return frontpage.pig()

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

@route('/assignment_notes')
def see_assignment_notes():
    return frontpage.assignment_notes()
	
@route('/assignment_notes/edit', method='POST')
def see_assignment_notes():
    return assignment_notes.notes_edit()

@route('/assignment_notes/update/:name', method='POST')
def update_assignment_notes(name):
    return assignment_notes.notes_update(name)

@route('/grade')
def grade():
    return grading.index()
    
@route('/gradeoneproblem')
def gradeoneproblem():
    return frontpage.gradeoneproblem()

@route('/startpage')
def startpage():
	return frontpage.startpage()
	
