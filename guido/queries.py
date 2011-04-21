#!/usr/bin/env python3

"""
Let's keep all of our SQL code in here, just for consistency and modularity.
Then in other files, go like:

queries.get_foo(username, assignment, problem)
"""

import sqlite3
import sort_probs

THEDB = 'guidodb'

def get_solution(student, assignment, problem):
    """Returns the solution associated with the given student's assignment
    and problem name"""
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
    """Returns all the assignmentids as a list, from the assignments in the db"""
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
    """Returns all the problems that have been submitted for a given assignment"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select name from Problem inner join Assignment on
                 Problem.assignmentid=Assignment.assignmentid where
                 Assignment.assignmentid=?"""
        c.execute(sql,(assignment,))
        all_problems = c.fetchall()

        stripped = []
        for problem in all_problems:
            stripped.append(problem[0])
        this = sort_probs.sort_prob(stripped)
        return this

def get_first_student(assignment, problemname):
    """Returns the first student, by alpha order, who submitted an assignment
    and problemname."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select username from Solution
                  where assignmentid=?
                  and problemname=?
                  order by username asc"""
        c.execute(sql, (assignment, problemname))
        result = c.fetchone()
        if result:
            return result[0]
        return None

def get_usernames(assignment, problemname):
    """Returns all usernames from a given assignment and problemname, that
    is all usernames that have submitted an answer."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select username from Solution
                  where assignmentid=?
                  and problemname=?"""
        c.execute(sql, (assignment, problemname))
        usernames = c.fetchall()
        stripped = []
        for name in usernames:
            stripped.append(name[0])
        return sorted(stripped)

def who_turned_in(assignment):
    """Returns all usernames from a given assignment, that
    is all usernames that have a submission."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select username from Submission
                  where assignmentid=?"""
        c.execute(sql, (assignment,))
        usernames = c.fetchall()
        stripped = []
        for name in usernames:
            stripped.append(name[0])
        return sorted(stripped)

def one_who_turned_in(assignment):
    """Returns all usernames from a given assignment, that
    is all usernames that have a submission."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select username from Submission
                  where assignmentid=?"""
        c.execute(sql, (assignment,))
        return c.fetchone()[0]

def get_graded_problems(assignment, username):
    """Returns a joined list of the solutions, grades, and comments for all
    graded problems for a given assignment and username"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select text, grade from Solution
                 where assignmentid=?
                 and username=?"""
        c.execute(sql, (assignment, username))
        request = c.fetchall()
        return request

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

def insert_problem_comment(comment, username, assignment, problemname):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    print("inserting comment {0} for {1}".format(comment, username))
    sql = ("insert into Comment "
           "(text, problemname, assignmentid) "
           "values (?, ?, ?) ")
    param = (comment, problemname, assignment)
    c.execute(sql, param)
    conn.commit()

    commentid = c.lastrowid
    sql = ("insert into CommentSolution "
           "(commentid, username, assignmentid, problemname) "
           "values (?, ?, ?, ?) ")
    param = (commentid, username, assignment, problemname)
    c.execute(sql, param)
    conn.commit()
    c.close()

def get_assignment_notes(assignment):
    with sqlite3.connect(THEDB)as conn:
        c = conn.cursor()
        sql = """select notes from Assignment
                 where assignmentid=?"""
        c.execute(sql, (assignment,))
        request = c.fetchone()
        return request[0]

