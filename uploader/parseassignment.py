#!/usr/bin/env python

"""
Routines to find the different problems in an assignment.
"""

import re
from collections import defaultdict

def get_answers(path):
    """Returns a dictionary from problem ids to the whole text of the student's
    response for that problem."""
    
    text = open(path, "r").read()
    text = text.replace("\r", "")
    lines = text.split("\n")

    out = defaultdict(lambda: "")
    pat = re.compile("^;; \[Problem (.\S*)\].*")

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
