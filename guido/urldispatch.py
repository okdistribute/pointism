#!/usr/bin/env python3

from bottle import route
from bottle import static_file
from bottle import request, redirect
from bottle import template

"""
This module handles all of the URL dispatching for Guido, mapping from URLs to
the functions that will be called in response.
"""

import grading
import frontpage
import assignment_notes
import queries

@route('/')
def index():
    return frontpage.startpage()

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

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
    grade = request.forms.get('grade')
    queries.insert_problem_grade(grade, username, assignment, problemname)
    comment = request.forms.get('comment')
    queries.insert_problem_comment(comment, username, assignment, problemname)
    return grading.grade(username, assignment, problemname)

@route('/grade_whole/:assignment/:username')
def grade_whole_submissions(assignment, username):
    return grading.whole_submission(assignment, username)

@route('/grade_whole/:assignment/:username', method='POST')
def grade_whole_submissions(assignment, username):
    grade = request.forms.get('grade')
    queries.insert_problem_grade(grade, username, assignment, None)
    comment = request.forms.get('comment')
    selectedtext=""
    queries.insert_problem_comment(comment, username, assignment, None)
    return grading.whole_submission(assignment, username)

#############################################################
# Viewing a specific report, picking an assignment/username #
#############################################################

@route('/specific_report')
def submission_report():
    return frontpage.submission_report()

@route('/specific_report/pick_username', method='POST')
def picked_assignment():
    """Called after the user has picked an assignment report"""
    aid = request.forms.get('assignment')
    redirect("/specific_report/%s" % aid)

@route('/specific_report/:assignment')
def submission_report(assignment):
    return frontpage.submission_report_choice(assignment)

@route('/specific_report/:assignment', method='POST')
def submission_report(assignment):
    username = request.forms.get('username')
    redirect("/specific_report/%s/%s" % (assignment, username))

@route('/specific_report/:assignment/:username')
def submission_report(assignment, username):
    return grading.submission_report(assignment, username)

################################
# Editing the assignment notes #
################################

@route('/assignment_notes')
def see_assignment_notes():
    return frontpage.assignment_notes()
	
@route('/assignment_notes/edit', method='POST')
def see_assignment_notes():
    return assignment_notes.notes_edit()

@route('/assignment_notes/update/:name', method='POST')
def update_assignment_notes(name):
    return assignment_notes.notes_update(name)

#####################################################################
# Picking a submission to grade, assuming problems have been graded #
#####################################################################

@route('/specific_submission')
def specific_submission():
    """Called after the user has picked that they want to grade a
    whole submission"""
    return frontpage.specific_submission()

@route('/specific_submission', method='POST')
def specific_submission():
    """Called after the user has picked which submission they want to
    grade. Redirects to /grade/assignment/username"""
    aid = request.POST.get('assignment','').strip()
    first = queries.one_who_turned_in(aid)
    redirect("/grade/%s/%s" % (aid, first))

###################################################
# Picking an assignment and then problem to grade #
###################################################

@route('/specific_problem')
def specific_post():
    return frontpage.specific_assignment()

@route('/specific_problem/pick_problem', method='POST')
def picked_assignment():
    """Called after the user has picked an assignment to grade"""
    aid = request.forms.get('assignment')
    redirect("/specific_problem/%s" % aid)
    
@route('/specific_problem/:aid')
def specific_problem_choice(aid):
    """Routed to after the user has picked an assignment to grade"""
    return frontpage.specific_problem_choice(aid)

@route('/specific_problem/:aid', method='POST')
def specific_problem_choice(aid):
    """Called after the user has picked an assignment and problem to
    grade. Redirects to grade/aid/problemname/username"""
    problemname = request.POST.get('problem','').strip()
    first = queries.get_first_student(aid, problemname)
    redirect("/grade/%s/%s/%s" % (aid, problemname, first))

#####################################################
## Making sure the user doesn't get an error screen #
#####################################################

@route('/grade')
def grade():
    redirect('/specific_problem')

@route('/grade', method='POST')
def grade_post():
    redirect('/specific_problem')

#########
# other #
#########


@route('/startpage')
def startpage():
    return frontpage.startpage()

@route('/none')
def unsupported():
    return template("unsupported")
