#!/usr/bin/env python3

"""
Main upload script for Guido.

Finds both the student submission and the autograder output for each problem in
this assignment.
"""

import sys
import sqlite3

import autograder
import parseassignment

THEDB = "../guidodb"
USAGE = "uploader.py <username> <assignment> <filename> [nodraft]"

def insert_submission(c, username, aid, hasdraft, text, autograder):
    print("saving {1} for {0}.".format(username, aid))
    sql = ("insert or replace into Submission "
           "(text, autograder, username, assignmentid, hasdraft) "
           "values (?, ?, ?, ?, ?)")
    param = (text, autograder, username, aid, hasdraft)
    insert_assignment(c, aid)
    c.execute(sql, param)

def insert_assignment(c, assignmentid):
    print("creating assignment {0}.".format(assignmentid))
    sql = ("insert or ignore into Assignment "
           "(assignmentid, notes) "
           "values (?, ?) ")
    param = (assignmentid, "(none)")
    c.execute(sql,param)

def insert_solution(c, username, aid, problemname, text, autograder):
    print("  ({0},{1},{2})".format(username,aid,problemname))
    sql = ("insert or replace into Solution "
           "(text, autograder, username, assignmentid, problemname) "
           "values (?, ?, ?, ?, ?) ")
    param = (text, autograder, username, aid, problemname)
    if(problemname != None):
        insert_problem(c, problemname, aid)
    c.execute(sql, param)

def insert_problem(c, name, aid):
    print("creating problem ({0}, {1})".format(aid, name))
    sql = ("insert or replace into Problem "
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

    hasdraft = True
    if len(sys.argv) == 5:
        hasdraft = sys.argv[4] is not "nodraft"

    #results = autograder.get_autograder_results(assignment, filename)
    results = autograder.fake_autograder_results(assignment, filename)
    answers = parseassignment.get_answers(filename)
    text = open(filename, "r").read()

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    
    insert_submission(c, username, assignment, hasdraft, text, "(none yet)")
    conn.commit()
    for key in answers.keys():
        insert_solution(c, username, assignment, key,
                        answers[key], results[key])
        conn.commit()
    c.close()

if __name__ == "__main__": main()
