#!/usr/bin/env python3

from bottle import template
from bottle import request
from bottle import redirect

import grading
import queries
import sqlite3
import model
from collections import defaultdict

THEDB = "guidodb"

def submission_report(assignment, username):
    query = queries.get_report(assignment, username)
    report = defaultdict(lambda: ('',[],''))
    ### problem = (problemname, code, comment, autograder)
    for problem in query:
        problemname = problem[0]
        code = problem[1]
        comment = problem[2]
        autograder = problem[3]     
        if(comment != None):
            commentlist = report[problemname][1]
            commentlist.append(comment)
            report[problemname] = (code, commentlist ,autograder)

    students = queries.who_turned_in(assignment)
    p,n = grading.find_prev_next(students, username)

    return template("submissionreport",
                    problems=report,
                    prevstudent=p,
                    nextstudent=n,
                    student=username,
                    assignment=assignment)

def framesbp(assignment, username):
    return template('framesbp', problems=grading.finalreport(assignment, username))
