#!/usr/bin/env python3

from bottle import template
from bottle import request
from bottle import redirect

import fakedata
import queries
import sqlite3
import model

THEDB = "guidodb"


def grade(username, assignment, problemname):
    solution = queries.get_solution(username, assignment, problemname)
    if(solution == None):
        redirect('/specific_assignment/' + assignment)
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]

    fullprevcomments = queries.get_all_past_comments()
    linenumbers = makelinenumbers(studentsolution)
    commenttext = queries.get_comment(username, assignment, problemname)

    students = queries.get_usernames(assignment, problemname)
    p,n = find_prev_next(students, username)
    
    return template("gradeoneproblem",
                    source=studentsolution,
                    existingcomment=commenttext,
                    linenumbers=linenumbers,
                    past_comments=fullprevcomments,
                    prevcomments=comments_firstline(fullprevcomments),
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    problem=problemname,
                    nextstudent=n,
                    prevstudent=p,
                    default_grade=get_grade(username, assignment, problemname), 
                    grades=possible_grades())

def submissionbyproblem(assignment, username):
    problems = []
    query = queries.get_graded_problems(assignment, username)
    for problem in query:
        problems.append(ProblemGrade(problem[0],problem[1]))

    fullprevcomments = queries.get_all_past_comments()

    students = queries.who_turned_in(assignment)
    p,n = find_prev_next(students, username)

    return template("gradesubmissionbyproblem",
                    problems=problems,
                    prevstudent=p,
                    nextstudent=n,
                    student=username,
                    assignment=assignment,
                    commenttext="",
                    grades=possible_grades(),
                    default_grade=get_grade(username, assignment, None),
                    existingcomment=None,
                    past_comments=fullprevcomments,
                    prevcomments=comments_firstline(fullprevcomments))

def whole_submission(assignment, username):
    solution = queries.get_submission(username, assignment)
    if(solution == None):
        redirect('/specific_assignment/' + assignment)
    studentsolution = solution[0]
    autograder_output = solution[1]
    grade = solution[2]

    fullprevcomments = queries.get_all_past_comments()
    linenumbers = makelinenumbers(studentsolution)

    students = queries.who_turned_in(assignment)
    p,n = find_prev_next(students, username)
    
    return template("gradesubmission",
                    source=studentsolution,
                    existingcomments=queries.get_all_comments(username, assignment),
                    linenumbers=linenumbers,
                    past_comments=fullprevcomments,
                    prevcomments=comments_firstline(fullprevcomments),
                    autograder=autograder_output,
                    student=username,
                    assignment=assignment,
                    nextstudent=n,
                    prevstudent=p,
                    default_grade=get_grade(username, assignment, None),
                    grades=possible_grades())


def submission_report(assignment, username):
    problems = []
    query = queries.get_report(assignment, username)
    for problem in query:
        problems.append(ProblemReport(problem[0],problem[1],problem[2]))

    students = queries.who_turned_in(assignment)
    p,n = find_prev_next(students, username)

    return template("submissionreport",
                    problems=problems,
                    prevstudent=p,
                    nextstudent=n,
                    student=username,
                    assignment=assignment)

def possible_grades():
    """Returns the possible grades (as a list of strings) for a given
    assignment. For now, this always returns A-F."""
    return  ("A", "B", "C", "D", "F")

def get_grade(username, assignment, problemname):
    """This method returns the grade given a username, assignment, and
    problemname. If you've graded this problem previously, we return
    the current grade.  This returns "A" if the autograder output
    returns True (or passed); else, return "F"."""
    if(problemname==None):
        solution = queries.get_submission(username, assignment)
    else:
        solution = queries.get_solution(username, assignment, problemname)

    if(solution != None):
        grade = solution[2]
    else:
        grade = "C"

    #if has already been graded, return that grade, converting from an integer.
    #to a string within the possible_grades range. This assumes
    #a 3-7 grading scale, where 3 is F and 7 is A.
    if((grade != None) & isinstance(grade, int)): 
        return possible_grades()[(len(possible_grades()) - grade) + 2]
    else: 
        return grade

class ProblemGrade:
    def __init__(self, source,grade):
        self.source = source
        self.grade = grade

class ProblemReport:
    def __init__(self, source, comment, autograder):
        self.source = source
        self.comment = comment
        self.autograder = autograder


def comments_firstline(list_of_prevcommenttext):
    prevcomments = list( map( lambda pair: model.Comment(pair[0],pair[1]),
                              zip(range(len(list_of_prevcommenttext)),
                                  list_of_prevcommenttext)) )
    return prevcomments

def makelinenumbers(text):
    """Given some text, generate line numbers to go on the left side of that
    text. Output is a string with newlines in it."""
    nlines = text.count("\n")
    numbers = "\n".join(map(str, range(1, nlines+1)))
    return numbers

def find_prev_next(students, current):
    """Out of a list of students, return the previous student and next student
    relative to the current student, out of the list of who turned in the
    current problem."""
    index = students.index(current)
    prevstudent = students[index - 1] if index != 0 else None
    nextstudent = students[index + 1] if index != (len(students) - 1) else None
    return (prevstudent, nextstudent)
