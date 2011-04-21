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
    redirect('/specific_problem')

@route('/grade', method='POST')
def grade_post():
    redirect('/specific_problem')

@route('/specific_problem')
def specific_post():
    return specific_problem.specific_assignment()

@route('/specific_problem/pick_problem', method='POST')
def picked_assignment():
    """Called after the user has picked an assignment to grade"""
    aid = request.POST.get('assignment','').strip()
    redirect("/specific_problem/%s" % aid)
    
@route('/specific_problem/:aid')
def specific_problem_choice(aid):
    """Routed to after the user has picked an assignment to grade"""
    return specific_problem.specific_problem_choice(aid)

@route('/specific_submission')
def specific_submission():
    """Called after the user has picked that they want to grade a
    whole submission"""
    return specific_problem.specific_submission()

@route('/specific_submission', method='POST')
def specific_submission():
    """Called after the user has picked which submission they want to
    grade. Redirects to /grade/assignment/username"""
    aid = request.POST.get('assignment','').strip()
    first = queries.one_who_turned_in(aid)
    redirect("/grade/%s/%s" % (aid, first))

@route('/specific_problem/:aid', method='POST')
def specific_problem_choice(aid):
    """Called after the user has picked an assignment and problem to
    grade. Redirects to grade/aid/problemname/username"""
    problemname = request.POST.get('problem','').strip()
    first = queries.get_first_student(aid, problemname)
    redirect("/grade/%s/%s/%s" % (aid, problemname, first))

@route('/grade/:assignment/:problemname/:username')
def grade_problem(username, assignment, problemname):
    """Routes the user to the grading page for and assignment, problem,
    username"""
    return grading.grade(username, assignment, problemname)

@route('/grade/:assignment/:username')
def grade_submission_with_graded_problem_table(assignment, username):
    """Routes the user to the grading an assignment page for and
    assignment, username, assuming the problems have been graded"""
    return grading.submissionbyproblem(assignment, username)

@route('/grade/:assignment/:problemname/:username', method='POST')
def grade_problem(username, assignment, problemname):
    """inserts a problem grade (when there's been a post) and routes back
    to the same page"""
    grade = request.POST.get('grade','').strip()
    queries.insert_problem_grade(grade, username, assignment, problemname)
    comment = request.POST.get('comment','').strip()
    queries.insert_problem_comment(comment, username, assignment, problemname)
    return grading.grade(username, assignment, problemname)

@route('/grade/whole/:assignment/:username')
def grade_whole_submissions(assignment, username):
    return grading.whole_submission(assignment, username)

@route('/grade/whole/:assignment/:username', method='POST')
def grade_whole_submissions(assignment, username):
    return grading.whole_submission(assignment, username)

@route('/startpage')
def startpage():
    return frontpage.startpage()
