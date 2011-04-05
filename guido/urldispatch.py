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
    query = request.POST.get('query', '').strip()
    if not query:
        return "You didn't supply a search query."
    else:
        conn = sqlite3.connect(THEDB)
        c = conn.cursor()
        query = request.POST.get('query','').strip()
        c.execute('select notes from assignment where assignmentid ="%s"' % query)
        if len(c.fetchall()) == 0:
            return "Cannot find assignment named %s." % query
        else:
            c.execute('select notes from assignment where assignmentid ="%s"' % query)
            notes = c.fetchone()[0]
            conn.commit()
            conn.close()
            assign_name = query
            return frontpage.assignment_notes_edit(notes, assign_name)

@route('/assignment_notes/update/:name', method='POST')
def update_assignment_notes(name):
    query = request.POST.get('query','').strip()
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    update_data = (query, name)
    c.execute('update assignment set notes=? where assignmentid=?', update_data)
    conn.commit()
    conn.close()
    return "Assignment notes for assignment " + name + " have been updated to '" + query + "'"

@route('/grade')
def grade():
    return grading.index()
