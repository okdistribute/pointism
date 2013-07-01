#!/usr/bin/env python3

from bottle import template
from bottle import request
from bottle import redirect

import queries

from grading import letter_grades_to_numbers

def for_assignment(assignmentid):
    csv_grades = queries.get_usernames_grades(assignmentid)
    ## none_grades = list(filter((lambda x: x[1] == None), csv_grades))
    none_grades = [grade for grade in csv_grades
                         if grade[1] in [None, "?"]]
    return template("csv_grades",
                    assignment=assignmentid,
                    filtered_grades=filter_grades(csv_grades),
                    none_grades=none_grades)

def filter_grades(csv_grades):
    ## filtered_grades = list(filter((lambda x: x[1] != None), csv_grades))
    filtered_grades = [grade for grade in csv_grades
                             if grade[1] not in [None, "?"]]
    return [(username, letter_grades_to_numbers[grade])
            for (username, grade) in filtered_grades]
