#!/usr/bin/env python3

"""
This script adds all students from a given file into the Guido database.

The format of the file to be parsed is assumed to be in a csv form, as
follows: 
<id>, <location>, 
<lab section>, <lecture>, <last name>, <first>, <username>, <email suffix>
"""
import sys, sqlite3

USAGE = "addstudents.py <filename>"
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
    print('Adding Students:\n')

    while(line != ''):
        vars = line.split(',')
        id = vars[0]
        location = vars[1]
        lab = vars[2]
        lecture = vars[3]
        lastname = vars[4]
        firstname = vars[5]
        username = vars[6]
        email = vars[7]
        lab = lab[0:len(lab) -1]
        student = (username, email, lecture, lab, "")
        print(student)
        c.execute('insert into Student values (?,?,?,?,?)',student)
        line = file.readline()
        
    conn.commit()
    conn.close()
    file.close()
        
if __name__ == "__main__": main()    

