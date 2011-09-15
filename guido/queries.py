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

def get_submission(student, assignment):
    """Returns the solution associated with the given student's assignment
    and problem name"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select * from Submission
                 where username=?
                   and assignmentid=?"""
        c.execute(sql, (student,assignment))
        submission = c.fetchone()
        return submission


def get_comments(student, assignment, problem):
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
        comments = c.fetchall()
        stripped = []
        for c in comments:
            stripped.append(c[0])
        return stripped


def get_student_comments(student, assignment):
    """Returns the text associated with the given student's solution to a
    problem, or None if none is set."""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        commentsql = """select C.text from Comment C,CommentSolution CS
                         where CS.assignmentid=?
                           and CS.username=?
                           and CS.commentid = C.commentid"""
        c.execute(commentsql, (assignment,student))
        comments = c.fetchall()
        stripped = []
        for c in comments:
            stripped.append(c[0])
        return stripped
        

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
        if problemname == None:
            sql = """select username from Solution
                  where assignmentid=?                 
                  order by username asc"""
            c.execute(sql, (assignment, ))
        else:
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
    if grade == 'None':
        return
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

def insert_submission_grade(grade, username, assignment):
    if grade == 'None':
        return
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    print("inserting grade {0} for {1}".format(grade, username))
    sql = ("update Submission "
           "set grade=? "
           "where username=? and assignmentid=?")
    param = (grade, username, assignment)
    c.execute(sql, param)
    conn.commit()
    c.close()

def insert_problem_comment(comment, code, username, assignment, problemname):
    if comment == None or comment == 'None':
        return
    ##check to make sure comments that contain just whitespace won't get added
    if comment.replace(" ","") == "":
        return
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    sql = """select commentid, text from Comment 
           where text=?"""
    c.execute(sql, (comment,))
    request = c.fetchone()

    #if this will be a duplicate comment, use the original commentid 
    if request != None:
        commentid = request[0]
    else: #else, insert a new comment, and commentid is the last row added.
        print("inserting comment {0} for {1}".format(comment, username))
        sql = ("insert into Comment "
               "(text, problemname, assignmentid) "
               "values (?, ?, ?) ")
        param = (comment, problemname, assignment)
        c.execute(sql, param)
        conn.commit()
        commentid = c.lastrowid
    
    ##insert into commentsolution now
    sql = ("insert into CommentSolution "
           "(commentid, studentcode, username, assignmentid, problemname) "
           "values (?, ?, ?, ?, ?) ")
    param = (commentid, code, username, assignment, problemname)
    c.execute(sql, param)
    conn.commit()
    c.close()

def get_assignment_notes(assignment):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """select notes from Assignment
                 where assignmentid=?"""
        c.execute(sql, (assignment,))
        request = c.fetchone()
        return request[0]

def get_all_past_comments():
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql=  """SELECT DISTINCT C.commentid, C.text from Comment C 
                 left join CommentSolution CS
                 where C.commentid=CS.commentid"""
        c.execute(sql)
        return c.fetchall()

def get_report(assignment, username):
    """Returns a list of solution, comment, and autograder"""
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql=  """Select S.problemname, S.text, C.text, S.autograder 
                 from Solution S
                 left join CommentSolution CS, Comment C   
                 where S.assignmentid=? and S.username=?
                 and S.username=CS.username
                 and C.commentid=CS.commentid
                 and C.problemname=S.problemname"""
        c.execute(sql, (assignment, username))
        return c.fetchall()

def get_comment(commentid):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = """Select * from Comment where
                 Comment.commentid=?"""
        c.execute(sql, (commentid,))
        return c.fetchone()

def update_comment_text(commentid, text):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = ("""update Comment 
               set text=?
               where commentid=?""")
        param = (text, commentid)
        c.execute(sql, param)
        conn.commit()
        c.close()

def delete_comment(commentid):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = ("""delete from Comment 
               where commentid=?""")
        param = (commentid,)
        c.execute(sql, param)
        conn.commit()
        c.close()

def get_usernames_grades(assignmentid):
    with sqlite3.connect(THEDB) as conn:
        c = conn.cursor()
        sql = ("""select username, grade from Submission
               where assignmentid=?""")
        param = (assignmentid,)
        c.execute(sql, param)
        return c.fetchall()
