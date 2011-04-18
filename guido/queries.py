#!/usr/bin/env python3

"""
Let's keep all of our SQL code in here, just for consistency and modularity.
Then in other files, go like:

queries.get_foo(username, assignment, problem)
"""

import sqlite3

THEDB = 'guidodb'

def get_solution(student, assignment, problem):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select * from Solution
                 where username=?
                   and assignmentid=?
                   and problemname=?"""
        c.execute(sql, (student,assignment,problem))
        solution = c.fetchone()
        return solution

def get_comment(student, assignment, problem):
    """Returns the text associated with the given student's solution to a
    problem, or None if none is set."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        commentsql = """select C.text from Comment C,CommentSolution CS
                         where CS.assignmentid=?
                           and CS.problemname=?
                           and CS.username=?
                           and CS.commentid = C.commentid"""
        c.execute(commentsql, (assignment,problem,student))
        existingcomment = c.fetchone()
        if existingcomment:
            return existingcomment[0]
        else:
            return None



def get_assignments():
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        assignment_sql = "select assignmentid from Assignment"
        c.execute(assignment_sql)
        assignments = c.fetchall()
        stripped = []
        for ass in assignments:
            stripped.append(ass[0])
        return stripped

def get_problems(assignment):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select problemid from Problem inner join Assignment on
                 Problem.assignment=Assignment.assignmentid where
                 Assignment.assignmentid=?"""
        c.execute(sql,(assignment,))
        all_problems = c.fetchall()
        stripped = []
        for problem in all_problems:
            stripped.append(problem[0])
        return stripped
