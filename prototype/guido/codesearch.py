import operator, os, pickle, sys, time, datetime, re 
## Add this directory to the Python path. It would be better, maybe, to do this
## with WSGIPythonPath in the apache config.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

sys.path.append("/opt/python-2.5/lib/python2.5/site-packages")
import cherrypy
from formencode import Invalid
from genshi.filters import HTMLFormFiller
from genshi.core import Markup

from lib import ajax, template
from database import mysql
from model import PreviousComment
from guido_page import GuidoPage
from form import QuestionGradingForm

class CodeSearch(GuidoPage):
    @cherrypy.expose
    @template.output('codesearch.html')
    def index(self, assignment=None, student=None, query=None):
        roles = ['admin', 'ta']
        self.page_for(roles)
        self.g_user = cherrypy.session.get('g_user')

        codeblocks = []
        if (assignment and student and query and present(student,assignment)):
            needle = str(query)
            student = str(student)
            assignment = str(assignment)
            codeblocks = getcodeblocks(student,assignment,query)

        header=Markup('code search')
        ipath=Markup('code search')
        return template.render(codeblocks=codeblocks,
                               ipath=ipath,
                               header=header)

def present(student,assignment):
    """Given a student username, and assignment name, are there any Answers
    that match those?"""

    db = mysql.DB()
    query = """
        SELECT ans.a_no FROM Answers ans, Questions q,
                             Associated_with assoc, Assignment a
         WHERE  q.q_no = assoc.q_no
           AND  ans.q_no = q.q_no
           AND  assoc.s_no = a.s_no
           AND  ans.student_id = %s
           AND  a.name = %s
        ORDER BY ans.a_no DESC""" 
    result = db.fetchone(query, (student,assignment))
    out = False
    if result:
        out = True
    db.close()
    return out

class Codeblock(object):
    def __init__(self, text):
        self.text = text
        nlines = text.count("\n")
        numbers = "\n".join(map(str, range(1, nlines+1)))
        self.linenumbers = numbers

def getcodeblocks(student,assignment,needle):
    """Given a student username, and assignment name, and a question name, get
    the most recent answer that matches those parameters."""

    db = mysql.DB()
    needle = "%" + needle + "%"
    query = """
        SELECT ans.* FROM Answers ans, Questions q,
                          Associated_with assoc, Assignment a
         WHERE  q.q_no = assoc.q_no
           AND  ans.q_no = q.q_no
           AND  assoc.s_no = a.s_no
           AND  ans.student_id = %s
           AND  a.name = %s
           AND  ans.text LIKE %s
        ORDER BY q.q_no ASC
        """ 
    results = db.do_query(query, (student,assignment, '%'+needle+'%'))
    out = []
    for result in results:
        text = result['text']
        out.append(Codeblock(text))
    db.close()
    return out
