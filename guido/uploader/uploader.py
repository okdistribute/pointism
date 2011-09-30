#!/usr/bin/env python3

"""
Main upload script for Guido.

Finds both the student submission and the autograder output for each problem in
this assignment.
"""

import sys
import sqlite3

import magsautograder
import parseassignment

THEDB = "../guidodb"
USAGE = "uploader.py <username> <assignment> <filename> <lab> [nodraft]"

def insert_submission(c, username, aid, lab, text, autograder):
    print("submitting {1} for {0}.".format(username, aid))
    sql = ("insert or replace into Submission "
           "(text, autograder, username, assignmentid) "
           "values (?, ?, ?, ?)")
    param = (text, autograder, username, aid)
    insert_assignment(c, aid)
    c.execute(sql, param)
    sql = ("select * from Student "
           "where username=?")
    c.execute(sql, (username,))
    student = c.fetchone()
    
    if(student == None):
        sql = ("insert into Student "
               "(lab, email, lecture, username) "
               "values (?, ?, ?, ?) ")
        param = (lab, username + "@indiana.edu", "Unknown", username)
    else:
        sql = ("update Student "
               "set lab=? "
               "where username=? ")
        param = (lab, username)
    c.execute(sql, param)
        

def insert_assignment(c, assignmentid):
    sql = ("insert or ignore into Assignment "
           "(assignmentid, notes) "
           "values (?, ?) ")
    param = (assignmentid, "(none)")
    c.execute(sql,param)

def insert_solution(c, username, aid, problemname, text, autograder, grade):
    print("  ({0},{1},{2})".format(username,aid,problemname))
    sql = ("insert or replace into Solution "
           "(text, autograder, username, assignmentid, problemname, grade) "
           "values (?, ?, ?, ?, ?, ?) ")
    param = (text, autograder, username, aid, problemname, grade)
    if(problemname != None):
        insert_problem(c, problemname, aid)
    c.execute(sql, param)

def insert_problem(c, name, aid):
    print("creating problem ({0}, {1})".format(aid, name))
    sql = ("insert or ignore into Problem "
           "(name, assignmentid, problemtext, notes) "
           "values (?, ?, ?, ?) ")
    param = (name, aid, "(unknown)", "(none)")
    c.execute(sql,param)

def main():
    if len(sys.argv) not in (4,5):
        print(USAGE)
        return
    username = sys.argv[1]
    assignment = sys.argv[2]
    filename = sys.argv[3]
    lab = sys.argv[4]

    upload_submission(username, assignment, filename, lab)

def upload_submission(username, assignment, filename, lab):
    #results = autograder.get_autograder_results(assignment, filename)
    results = magsautograder.fake_autograder_results(assignment, filename)

    text = open(filename, "r").read()

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    
    insert_submission(c, username, assignment, lab, text, "(none yet)")

    conn.commit()
    c.close()

if __name__ == "__main__": main()
