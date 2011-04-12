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

Problem = """\
create table if not exists Problem (
    name text not null,
    assignmentid text not null,
    problemtext text,
    notes text,
    primary key(assignmentid, name),
    foreign key(assignmentid) references Assignment(assignmentid)
)"""

Assignment = """\
create table if not exists Assignment (
    assignmentid text primary key,
    notes text
)"""

## key for a Solution is Student,Assignment,Problem
Solution = """\
create table if not exists Solution (
    text text,
    autograder text,
    grade integer,
    username text,
    assignmentid text,
    problemname text,
    foreign key(username) references Student(username),
    foreign key(problemname) references Problem(name),
    foreign key(assignmentid) references Assignment(assignmentid),
    primary key(username, assignmentid, problemname)
)"""

Submission = """\
create table if not exists Submission (
    text text,
    autograder text,
    grade integer,
    notes text,
    hasdraft boolean,
    username text,
    assignmentid text,
    problemname text,
    foreign key(username) references Student(username),
    foreign key(problemname) references Problem(name),
    foreign key(assignmentid) references Assignment(assignmentid)
)"""

Comment = """\
create table if not exists Comment (
    commentid integer primary key autoincrement,
    text text,
    problemname text,
    assignmentid text,
    foreign key(problemname) references Problem(name),
    foreign key(assignmentid) references Assignment(assignmentid)
)"""

CommentSolution = """\
create table if not exists CommentSolution (
    id integer primary key autoincrement,
    commentid integer,
    username text,
    assignmentid text,
    problemname text,
    foreign key(username) references Student(username),
    foreign key(problemname) references Problem(name),
    foreign key(assignmentid) references Assignment(assignmentid)
)"""

tables = [Student,
Assignment,
Solution,
Problem,
Submission,
Comment,
CommentSolution
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
        try:
            c.execute(sql)
        except Exception as e:
            print("*** exception!!! ***")
            print(sql)
            print(e)
            print("failed!")
            return
        conn.commit()
    print("ok done.")
    c.close()

if __name__ == "__main__": main()
