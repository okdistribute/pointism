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

import sys, sqlite3, re

USAGE = "autograder.py <filename>"
THEDB = "guidodb"

def main():
    
    if len(sys.argv) != 2:
        print(USAGE)
        return

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    
    file = open(sys.argv[1])
    #need to make sure file exists
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
                add_to_db(grader_problem)
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
    grader_problem = (number, name, result, output)
    add_to_db(grader_problem)


def add_to_db(grader_problem):
    """Takes in (number, name, result, output) and inputs into db"""
    print(grader_problem)

            

if __name__ == "__main__": main()
