#!/usr/bin/env python3

from bottle import template
from bottle import request

import fakedata
import autograder
import queries
import sqlite3

THEDB="guidodb"

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

def grade(username, assignment, problemname):
    solution = queries.get_solution(username, assignment, problemname)
    if(solution == None):
        return "There is nothing to see here"
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]

    prevcomments = fakedata.prevcomments
    linenumbers = makelinenumbers(studentsolution)
    commenttext = queries.get_comment(username, assignment, problemname)

    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomment=commenttext,
                    linenumbers=linenumbers,
                    prevcomments=prevcomments,
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    default_grade=get_grade(username, assignment, problemname), 
                    grades=possible_grades())

def insert_problem_grade(grade, username, assignment, problemname):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    print("inserting grade {0} for {1}".format(grade, username))
    sql = ("update Solution "
           "set grade=? "
           "where username=? and assignmentid=? and problemname=? ")
    param = (grade, username, assignment, problemname)
    c.execute(sql, param)
    conn.commit()
    c.close()

def next_student():
    return ""

def possible_grades():
    """Returns the possible grades (as a list of strings) for a given
    assignment. For now, this always returns A-F."""
    return  ("A", "B", "C", "D", "F")

def get_grade(username, assignment, problemname):
    """This method returns the grade given a username, assignment, and
    problemname. If you've graded this problem previously, we return
    the current grade.  This returns "A" if the autograder output
    returns True (or passed); else, return "F"."""
    solution = queries.get_solution(username, assignment, problemname)

    if(solution != None):
        grade = solution[2]
    else:
        grade = "C"

    #if has already been graded, return that grade, converting from an integer.
    #to a string within the possible_grades range. This assumes
    #a 3-7 grading scale, where 3 is F and 7 is A.
    if((grade != None) & isinstance(grade, int)): 
        return possible_grades()[(len(possible_grades()) - grade) + 2]
    else: 
        return grade
