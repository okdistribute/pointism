#!/usr/bin/env python3

from bottle import route
from bottle import static_file
from bottle import request, redirect

"""
This module handles all of the URL dispatching for Guido, mapping from URLs to
the functions that will be called in response.
"""

import grading
import frontpage
import assignment_notes
import specific_problem
import queries

@route('/')
def index():
    return frontpage.startpage()

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
    redirect('/specific_assignment')

@route('/grade', method='POST')
def grade_post():
    redirect('/specific_assignment')

@route('/specific_assignment')
def specific_post():
    return specific_problem.specific_assignment()

@route('/specific_assignment/pick_problem', method='POST')
def picked_assignment():
    aid = request.POST.get('assignment','').strip()
    redirect("/specific_assignment/%s" % aid)
    
@route('/specific_assignment/:aid')
def specific_problem_choice(aid):
    return specific_problem.specific_problem_choice(aid)

@route('/specific_assignment/:aid', method='POST')
def specific_problem_choice(aid):
    problemname = request.POST.get('problem','').strip()
    first = queries.get_first_student(aid, problemname)
    redirect("/grade/%s/%s/%s" % (aid, problemname, first));

@route('/grade/:assignment/:problemname/:username')
def grade_problem(username, assignment, problemname):
    return grading.grade(username, assignment, problemname)

@route('/grade/:assignment/:username')
def grade_assignment(assignment, username):
    return grading.grade_assignment(assignment, username)

@route('/grade/:assignment/:problemname/:username', method='POST')
def grade_problem(username, assignment, problemname):
    grade = request.POST.get('grade','').strip()
    grading.insert_problem_grade(grade, username, assignment, problemname)
    return grading.grade(username, assignment, problemname)

@route('/startpage')
def startpage():
    return frontpage.startpage()
