import sys, sqlite3

def main():
    assignment_name = sys.argv[1]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    name = (assignment_name,"")
    c.execute('insert into assignment values (?,?)',name)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
