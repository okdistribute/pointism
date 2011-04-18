from bottle import template
from bottle import route
from bottle import request

import queries
import sqlite3

THEDB = "guidodb"

def specific_assignment():
    return template("specific_problem",assignments=queries.get_assignments())

def specific_problem_choice():
    query = request.POST.get('assignment','').strip()
    return template("specific_problem_choice",problems=queries.get_problems(query))
