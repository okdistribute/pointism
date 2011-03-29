#!/usr/bin/env python3

from bottle import template

import fakedata

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

    autograder=fakedata.autograder
    studentsolution = fakedata.studentsolution
    existingcomment = fakedata.existingcomment
    prevcomments = fakedata.prevcomments

    linenumbers = makelinenumbers(studentsolution)
    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomment=existingcomment,
                    linenumbers=linenumbers,
                    prevcomments=prevcomments,
                    autograder=autograder,
                    student=fakedata.student,
                    assignment=fakedata.assignment)

