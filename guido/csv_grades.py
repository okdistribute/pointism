#!/usr/bin/env python3

from bottle import template
from bottle import request
from bottle import redirect

import queries

def for_assignment(assignmentid):
    csv_grades = queries.get_usernames_grades(assignmentid)

    filtered_grades = list(filter((lambda x: x[1] != None), csv_grades))
    none_grades = list(filter((lambda x: x[1] == None), csv_grades))

    grades_to_numbers = {'A' : 7,
                         'B' : 6,
                         'C' : 5,
                         'D' : 4,
                         'F' : 3 }

    filtered_grades = list(map((lambda x: (x[0], grades_to_numbers[x[1]])),filtered_grades))

    return template("csv_grades",
                    assignment=assignmentid,
                    filtered_grades=filtered_grades,
                    none_grades=none_grades)
    

    
