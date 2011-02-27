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
