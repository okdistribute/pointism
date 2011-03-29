#!/usr/bin/env python3

import sys, sqlite3

THEDB = "guidodb"

def main():
    assignment_name = sys.argv[1]
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    name = (assignment_name,"")
    print(name)
    c.execute('insert into Assignment values (?,?)',name)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
