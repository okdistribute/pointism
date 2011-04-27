from bottle import template
from bottle import route
from bottle import request

import queries


def specific_assignment():
    return template("specific_problem",assignments=queries.get_assignments())

def specific_problem_choice(aid):
    return template("specific_problem_choice",problems=queries.get_problems(aid))

def specific_submission():
    return template("specific_submission",assignments=queries.get_assignments())

def submission_report():
    return template("specific_report",assignments = queries.get_assignments())

def submission_report_choice(aid):
    return template("specific_report_choice",usernames = queries.who_turned_in(aid))
