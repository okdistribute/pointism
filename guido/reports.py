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
    submission,autograder,grade = queries.get_report(assignment, username)
    comments = queries.get_submission_comments(assignment, username)
    
    students = queries.who_turned_in(assignment)
    p,n = grading.find_prev_next(students, username)
    
    return template("gradingreport",
                    prevstudent=p,
                    nextstudent=n,
                    student=username,
                    assignment=assignment,
                    source=submission,
                    grade=grade,
                    autograder=autograder,
                    linenumbers=grading.makelinenumbers(submission),
                    existingcomments=grading.dictify(comments))

def send_report(aid, username):
    """sends the most current report for the given assignment to the
    given username"""
    print("sending %s report to %s." % (aid, username))
    email = get_email(username)
    report = queries.get_report(aid, username)
    send_report_to_email(report, email)

def send_assignment_reports(aid):
    """grabs all users who have a submission for the given assignment
    and then sends a report for each student"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select username from Submission
                 where assignmentid=?"""
        c.execute(sql, (assignment,))
        usernames = c.fetchall()
        for u in usernames:
            send_report(aid, u)

def get_email(username):
    """gets the email address for a given username"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select Student.email from Student
                 where username=?"""
        c.execute(sql, (username,))
        email = c.fetchone()
        return email

def send_report_to_email(report, email):
    """sends the most current report for the given assignment to the
    given email."""    
    this = "not implemented. should throw an error."
