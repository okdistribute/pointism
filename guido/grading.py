#!/usr/bin/env python3

from bottle import template
from bottle import request

import fakedata
import autograder
import sqlite3

THEDB = 'guidodb'

def makelinenumbers(text):
    """Given some text, generate line numbers to go on the left side of that
    text. Output is a string with newlines in it."""
    nlines = text.count("\n")
    numbers = "\n".join(map(str, range(1, nlines+1)))
    return numbers

def index():
    # Template for grading a single problem wants to know...
    # - is this a get or a post? ie, did you just commit a grade for a problem?
    # - if you've graded this problem previously, what's the current grade? (look
    #   that up in the database)
    # - otherwise, what's the default grade? if autograder output is correct,
    # then default to A, else F.
    # - if you've graded this problem previously, what were the comments you
    #   gave? (text that you pulled for a specific comment id in the database.)
    # - what's the answer the student gave?
    # - what's the autograder output for that answer?

    studentsolution = fakedata.studentsolution
    autograder_output = fakedata.autograder
    existingcomment = fakedata.existingcomment
    prevcomments = fakedata.prevcomments

    linenumbers = makelinenumbers(studentsolution)    

    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomment=existingcomment,
                    linenumbers=linenumbers,
                    prevcomments=prevcomments,
                    autograder=autograder_output,
                    student=fakedata.student,
                    assignment=fakedata.assignment,
                    default_grade=default_grade(), 
                    grades=possible_grades())

def grade(assignment, problemname):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()

    sql = "SELECT * from Solution WHERE assignmentid='%s' AND problemname='%s'" % (assignment, problemname)
    c.execute(sql)
    solution = c.fetchone()
    if(solution == None):
        return "There is nothing to see here"
    
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]
    notes = solution[3]
    hasdraft = solution[4]
    username = solution[5]
        
    commentsql = "SELECT * from CommentSolution WHERE assignmentid='%s' AND problemname='%s' AND username='%s'" % (assignment, problemname, username)
    c.execute(commentsql)
    existingcomment = c.fetchone()

    prevcomments = fakedata.prevcomments
    linenumbers = makelinenumbers(studentsolution)

    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomment=existingcomment,
                    linenumbers=linenumbers,
                    prevcomments=prevcomments,
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    default_grade=default_grade(), 
                    grades=possible_grades())

def next_student():
    return ""

def possible_grades():
    """Returns the possible grades (as a list of strings) for a given
    assignment. For now, this always returns A-F."""
    return  ("A", "B", "C", "D", "F")

def default_grade():
    """Returns the default grade as a string. For now, this always
    returns "C". We will want this to return "A" if the autograder
    output returns True (or passed); else, return "F"."""
    return "C"
