#!/usr/bin/env python

"""
Routines to run the autograder.
"""

import os
import re
import commands
import tempfile
from collections import defaultdict

def runtests(assignment, path):
    """Run the autograder on the given file. Returns the output. """

    cmd = ("env SCHEMEHEAPDIRS=/l/ChezScheme-7.4d/lib/csv7.4d/i3le ./sgrade-scheme/sg.ss %s < %s" % (assignment, path))
    output = commands.getoutput(cmd)
    return output


def build_map(grader_output):
    """Takes a string of output from the autograder and returns a map from
    problem identifiers (like "Problem 9" or "Problem 1b") to the autograder
    output from that problem."""

    pat = re.compile("Problem (.*):.*-->.*")

    out = defaultdict(lambda: "")
    lines = grader_output.split("\n")

    current_id = None
    current_output = ""

    for line in lines:
        match = pat.match(line)
        if match:
            if current_id:
                out[current_id] += current_output
            current_id = match.group(1)
            current_output = (line + "\n")
        else:
            current_output += (line + "\n")
    out[current_id] += current_output

    return out

def get_autograder_results(assignment, path):
    """Function that you should call. Takes an assignment ID and a path for a
    student solution to that assignment. Returns a dictionary from problem IDs
    to the autograder output for that problem."""

    output = runtests(assignment, path)
    return build_map(output)

def fake_autograder_results(assignment, path):
    return defaultdict(lambda:"",
        {'11': 'Problem 11: both-odd?  -->   correct:  1/1\n',
         '10': 'Problem 10: pick-one-at-random -->   correct: 1/1\n',
         '12': 'Problem 12: either-even? -->   correct:  1/1\n',
         'EC1': 'Problem EC1: least    -->   correct:  1/1\n',
         '1': 'Problem 1: least    -->   correct:  1/1\n',
         '1a': 'Problem 1a: least    -->   correct:  1/1\n',
         '1b': 'Problem 1b: least-of-three -->   correct:  1/1\n',
         '3': 'Problem 3: curious?  -->   correct: 1/1\n',
         '2': 'Problem 2: next-even -->   correct:  1/1\n',
         '5': 'Problem 5: opposite  -->   correct:  1/1\n',
         '4': 'Problem 4: sleep-in? -->   correct: 1/1\n',
         '7': 'Problem 7: next-collatz -->   correct:  1/1\n',
         '6': 'Problem 6: next-compass -->   correct:  1/1\n',
         '9': 'Problem 9: up-or-down -->   correct: 1/1\n',
         '8': 'Problem 8: dna-complement -->   correct:  1/1\n',
         '8a': 'Problem 8: dna-complement -->   correct:  1/1\n',
         '8a': 'Problem 8: dna-complement -->   correct:  1/1\n'}) 
