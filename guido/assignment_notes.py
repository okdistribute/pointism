from bottle import request
from bottle import template
import sqlite3

THEDB = "guidodb"

def notes_update(name):
    query = request.forms.get('query')
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    update_data = (query, name)
    c.execute('update assignment set notes=? where assignmentid=?', update_data)
    conn.commit()
    conn.close()
    return template("content", title="Success!", content="Assignment notes for assignment " + name + " have been updated to '" + query + "'")

def notes_edit():
    query = request.forms.get('assignment')
    if not query:
        return "You didn't supply a search query."
    else:
        conn = sqlite3.connect(THEDB)
        c = conn.cursor()
        c.execute('select notes from assignment where assignmentid ="%s"' % query)
        if len(c.fetchall()) == 0:
            return "Cannot find assignment named %s." % query
        else:
            c.execute('select notes from assignment where assignmentid ="%s"' % query)
            notes = c.fetchone()[0]
            conn.commit()
            conn.close()
            assign_name = query
            return template("assignment_notes_edit", notes_edit=notes, assignment_name=assign_name)
