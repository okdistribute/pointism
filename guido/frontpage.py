#!/usr/bin/env python3

from bottle import template
from bottle import route

def frontpage():
    return template("frontpage")

def cow():
    return template("cow")

def pig():
    return template("pig")

def assignment_notes():
    return template("assignment_notes")

def assignment_notes_edit(notes, assign_name):
    return template("assignment_notes_edit", notes_edit=notes, assignment_name=assign_name)
