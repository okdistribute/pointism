#!/usr/bin/env python3

from bottle import template
from bottle import request
from bottle import redirect
from collections import defaultdict

import queries
import model

letter_grades_to_numbers = {
    'A' : 7,
    'B' : 6,
    'C' : 5,
    'D' : 4,
    'F' : 1,
    'Z' : 'Z',
    '?' : None,
}

## reverse the mapping.
numbers_to_letter_grades = \
    dict((v,k) for k, v in letter_grades_to_numbers.items())

def grade(username, assignment, problemname):
    solution = queries.get_solution(username, assignment, problemname)
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]

    fullprevcomments = queries.get_all_past_comments()
    linenumbers = makelinenumbers(studentsolution)
    commenttext = queries.get_comments(username, assignment, problemname)
    students = queries.get_usernames(assignment, problemname)
    p,n = find_prev_next(students, username)
    
    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomments=commenttext,
                    linenumbers=linenumbers,
                    past_comments=list(map(lambda pair: pair[1], fullprevcomments)),
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    problem=problemname,
                    nextstudent=n,
                    prevstudent=p,
                    default_grade=get_grade(username, assignment, problemname), 
                    grades=possible_grades())

def submissionbyproblem(assignment, username):
    return template("unsupported")

def whole_submission(assignment, username, by_section):
    """by_section should be True or False, whether or not to get the
    first/last by section or not"""
    solution = queries.get_submission(username, assignment)
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]

    fullprevcomments = queries.get_all_past_comments()
    linenumbers = makelinenumbers(studentsolution)
    if(by_section):
        section = queries.get_section(username)
        students = queries.who_turned_in_by_section(assignment, section)
    else:
        students = queries.who_turned_in(assignment)
    p,n = find_prev_next(students, username)

    thecomments = dictify(queries.get_student_commentids(username, assignment))
    return template("grade_whole",
                    source=studentsolution,
                    past_comments=list(map(lambda pair: pair[1], fullprevcomments)),
                    existingcomments=thecomments,
                    linenumbers=linenumbers,
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    nextstudent=n,
                    prevstudent=p,
                    default_grade=get_grade(username, assignment, None),
                    grades=possible_grades())

def possible_grades():
    """Returns the possible grades (as a list of strings) for
    assignments. This returns A-F. TODO: user interface to change this
    based on assignment or for all assignments"""
    return  ("A", "B", "C", "D", "F", "Z", "?")

def get_grade(username, assignment, problemname):
    """This method returns the grade given a username, assignment, and
    problemname. If you've graded this problem previously, we return
    the current grade.  This returns "A" if the autograder output
    returns True (or passed); else, return "F"."""

    if(problemname==None):
        ## This happens when grading a whole submission at once.
        solution = queries.get_submission(username, assignment)
    else:
        ## This happens if we're just grading a single problem.
        solution = queries.get_solution(username, assignment, problemname)

    if solution is None or solution[2] is None:
        grade = "?"
    else:
        grade = solution[2]
    assert grade in letter_grades_to_numbers.keys(), grade
    return grade

def dictify(l):
    ret = {}
    for x,y in l:
        ret[x] = y
    return ret

def comments_firstline(idstext):
    prevcomments = list( map( lambda pair: model.Comment(pair[0],pair[1]), idstext))
    return prevcomments

def makelinenumbers(text):
    """Given some text, generate line numbers to go on the left side of that
    text. Output is a string with newlines in it."""
    nlines = text.count("\n")
    numbers = "\n".join(map(str, range(1, nlines+1)))
    return numbers.split("\n")

def find_prev_next(students, current):
    """Out of a list of students, return the previous student and next student
    relative to the current student, out of the list of who turned in the
    current problem."""
    index = students.index(current)
    prevstudent = students[index - 1] if index != 0 else None
    nextstudent = students[index + 1] if index != (len(students) - 1) else None
    return (prevstudent, nextstudent)
