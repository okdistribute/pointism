#!/usr/bin/env python3

"""
Initialize the guido database. Doesn't do anything if the db is already
there.
"""

import sqlite3
import datetime

THEDB = "guidodb"

## table schemas!
Student = """\
create table if not exists Student (
    username text primary key,
    email text not null,
    lecture text not null,
    lab text not null,
    notes text
)"""

## TODO(alexr): make assignment a foreign key into the assignments table.
## TODO(alexr): make the key for Problem be the assignment name and the problem
## name taken together.
Problem = """\
create table if not exists Problem (
    problemid int primary key,
    name text not null,
    assignment text not null,
    problemtext text,
    notes text
)"""

Assignment = """\
create table if not exists Assignment (
    assignmentid integer primary key autoincrement,
    name text
)"""

## key for a Solution is Student,Assignment,Problem
Solution = """\
create table if not exists Solution (
    solutionid integer primary key autoincrement,
    name text not null
)"""

Submission = """\
create table if not exists Submission (
    submissionid integer primary key autoincrement,
    name text not null
)"""

Comment = """\
create table if not exists Comment (
    commentid integer primary key autoincrement,
    text text
)"""

tables = [Student,
Problem,
Assignment,
Solution,
Submission,
Comment,
]

def main():
    """Initialize tables that we'll need if they're not already created and
    print out all the db contents, just to see what we have."""
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()

    # Create tables that we'll need.
    print("Creating guido tables...")
    for sql in tables:
        print("  creating", sql.split("\n")[0].split()[-2])
        c.execute(sql)
    print("ok done.")

    conn.commit()
    c.close()

if __name__ == "__main__": main()
