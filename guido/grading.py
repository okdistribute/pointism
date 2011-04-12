#!/usr/bin/env python3

from bottle import template

import fakedata
import autograder

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

    autograder_output = fakedata.autograder
    studentsolution = fakedata.studentsolution
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

def possible_grades():
    """Returns the possible grades (as a list of strings) for a given
    assignment. For now, this always returns A-F."""
    return  ("A", "B", "C", "D", "F")

def default_grade():
    """Returns the default grade as a string. For now, this always
    returns "C". We will want this to return "A" if the autograder
    output returns True (for passed); else, return "F"."""
    return "C"
