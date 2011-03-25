#!/usr/bin/env python3

"""
This script adds all students from a given file into the Guido database.

The format of the file to be parsed is assumed to be in a csv form, as
follows: 
<username>, <full name>, <lecture section>, <lab section>\n
"""
import sys

USAGE = "addstudents.py <filename>"

def main():

    if len(sys.argv) != 2:
        print(USAGE)
        return

    file = open(sys.argv[1])
    #need to make sure file exists

    line = file.readline()
    print('Adding Students:\n')

    while(line != ''):
        vars = line.split(',')
        username = vars[0]
        fullname = vars[1]
        lecture = vars[2]
        lab = vars[3]
        lab = lab[0:len(lab) -1]
        print('', username, fullname, lecture, lab)
        #need to insert into db 
        line = file.readline()

    file.close()
        
if __name__ == "__main__": main()    

