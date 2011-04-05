#!/usr/bin/env python3

"""
This script parses and adds the autograder output into the Guido database.

The format is assumed to be in the MAGS style, i.e.

<problem number>.<optional subnumbers>: <problem-name>: <result>
      <result specifics....>

The script parses each output between this form, records a pass or fail, and
enters that information into the database. It also saves the compelte autograder
output just in case it is needed.
"""

import sys, re, subprocess

    
def runtests(assignment, path):

    cmd = ("something")
    
    output = subprocess.getoutput(cmd)
    return output

def build(grader_output):

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    
    to_return = ()


    file = open(sys.argv[1])
    line = file.readline()
    line = file.readline()
    line = file.readline()
    pat = re.compile("(\d.*): (.*): (.*)")
    output = ''
    number = None
    name = None
    result = None
    getting_output = 0

    while (line != ''):
        ids = pat.match(line)
        if ids:
            if(getting_output == 1):
                getting_output = 0
                grader_problem = (number, name, result, output)
                to_return.append(grader_problem)
            number = ids.group(1)
            name = ids.group(2)
            result = ids.group(3)
        else:
            if(line == '\n'):
                line = ''
            if(getting_output == 1):
                output += line
            else:
                output = line
                getting_output = 1

        line = file.readline()
    #the last one still needs to be build and appended
    grader_problem = (number, name, result, output)
    to_return.append(grader_problem)


def get_autograder_results(assignment, path):
    """Function that you should call. Takes an assignment ID and a path for a
    student solution to that assignment. Returns a dictionary from problem IDs
    to the autograder output for that problem."""
    output = runtests(assignment, path)
    return build(output)
            

if __name__ == "__main__": main()
