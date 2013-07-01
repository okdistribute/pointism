#!/usr/bin/env python3

from bottle import template
from bottle import route

from bottle import template
from bottle import route
from bottle import request

import queries

def specific_assignment():
    return template("assignment_selection",
                    assignments=queries.get_assignments(),
                    title="Grade Specific Problem",
                    target="/specific_problem/pick_problem")

def specific_problem_choice(aid):
    return template("problem_selection",
                    problems=queries.get_problems(aid),
                    title="Grade Specific Problem",
                    target="")

def specific_submission():
    return template("assignment_selection",
                    assignments=queries.get_assignments(),
                    title="Grade Submission by Problem",
                    target="",
                    sections=queries.get_sections())

def submission_report():
    return template("assignment_selection",
                    assignments=queries.get_assignments(),
                    title="View Student Reports",
                    target="/gradingreport/pick_username",
                    sections=None)

def submission_report_choice(aid):
    return template("username_selection",
                    usernames=queries.who_turned_in(aid),
                    target="",
                    title="View a Report")

def assignment_notes():
    return template("assignment_selection", 
                    assignments=queries.get_assignments(),
                    target="/assignment_notes/edit",
                    title="Edit Assignment Notes",
                    sections=None)

def startpage():
    return template("startpage")

def grade_whole():
    return template("assignment_selection",
                    title="Grade Whole Submissions",
                    assignments=queries.get_assignments(),
                    target="",
                    sections=queries.get_sections())
                    
def csv_grades():
    return template("assignment_selection",
                    title="Export Grades to CSV",
                    target="/csv_grades",
                    assignments=queries.get_assignments(),
                    sections = None)

