#!/usr/bin/env python

"""
Main upload script for Guido.

Finds both the student submission and the autograder output for each problem in
this assignment.
"""

import sys
sys.path.append("..")
# sys.path.remove("/home/dikim/Genshi")

import guido.database.mysql as mysql
import autograder
import parseassignment

USAGE = "uploader.py <username> <assignment> <filename>"

def get_question_id(db, assignment, key):
    sql = """
SELECT q.q_no FROM Questions q, Associated_with assoc, Assignment a
 WHERE  q.q_no = assoc.q_no
   AND  assoc.s_no = a.s_no
   AND  a.name = %s
   AND  q.name = %s""" 
    results = db.do_query(sql, (assignment, key))
    if len(results) == 0:
        print "Couldn't find assignment %s, question %s." % (assignment,key)
        return None
    q_no = results[0]['q_no']
    return q_no

def main():
    if len(sys.argv) != 4:
        print USAGE
        return

    username = sys.argv[1]
    assignment = sys.argv[2]
    filename = sys.argv[3]

    #results = autograder.get_autograder_results(assignment, filename)
    results = autograder.fake_autograder_results(assignment, filename)
    answers = parseassignment.get_answers(filename)
    db = mysql.DB()

    for key in answers.keys():
        print "inserting %s, question %s." % (assignment, key)
        q_no = get_question_id(db, assignment, key)

        if q_no is None:
            print "skipping."
            continue

        sql = ("INSERT INTO Answers "
               "(q_no, student_id, text, autograder) "
               "VALUES (%s, %s, %s, %s)")
        param = (q_no, username, answers[key], results[key])
        db.do_commit(sql, param)
    db.close()

if __name__ == "__main__": main()
