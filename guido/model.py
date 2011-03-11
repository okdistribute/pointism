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

class Source(object):
    """Representation of student code"""
    def __init__(self, username, text):
        self.username = username
        self.grade = 0
        if len(text) > 0:
            self.text = text
        else:
            self.text = "(empty)"

    def grade(self, grade):
        self.grade = grade
        
class Student(object):
    """Representation of students"""
    def __init__(self, username, name, section):
        self.username = username
        self.name = name
        self.section = section
        


                 
