#!/usr/bin/env python3

"""
Objects that we want to store in the database.
"""

class Comment(object):
    """Quick representation of comments that have been stored in the database
    previously."""
    def __init__(self, commentid, content):
        self.commentid = commentid
        self.content = content
        self.firstline = ""
        if len(content) > 0:
            self.firstline = content.split("\n")[0]
        else:
            self.firstline = "(empty)"

class Assignment(object):
    """Representation of an assignment"""
    def __init__(self, id, name, text):
        self.id = id
        self.name = name
        if len(text) > 0:
            self.text = text
        else:
            self.text = "(empty)"
        
class Student(object):
    """Representation of students"""
    def __init__(self, username, name, section):
        self.username = username
        self.name = name
        self.section = section
        

class ProblemGrade(object):
    def __init__(self, source,grade):
        self.source = source
        self.grade = grade



                 
