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
from model import PreviousComment, FinalGrade
from guido_page import GuidoPage
from form import QuestionGradingForm

class GradingPage(GuidoPage):
    @cherrypy.expose
    @template.output('give_grade.html')
    def give_grade(self):
        roles = ['admin', 'final']
        self.page_for(roles)
        self.g_user = cherrypy.session.get('g_user')
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Final Grader: <a \
        href="give_grade2student">Students</a> > \
        <b>Give a grade to ???</b>')
        return template.render(ipath =ipath , header=header)

    @cherrypy.expose
    @template.output('give_grade2student.html')
    def give_grade2student(self):
        roles = ['admin', 'final']
        self.page_for(roles)
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' %
            (self.g_term, self.g_user.user_id))
        ipath=Markup('Final Grader: <b>Students</b> <font color="grey"> > \
        Give a grade </font>')
        return template.render(ipath =ipath , header=header)

    @cherrypy.expose
    @template.output('grading.html')
    def index(self, assignment=None, student=None, problem=None, **data):
        roles = ['admin', 'ta']
        self.page_for(roles)
        self.g_user = cherrypy.session.get('g_user')

        text = ""
        autograder = ""
        existingcomment = ""
        err = None

        ## Get TA's username and load Answer from the db.
        ta = self.g_user.user_id
        ans = get_answer(student, assignment, problem)
        student_ids = get_student_ids(assignment, problem)
        final_grade = build_final_grade(student, student_ids)

        prevcomments = []

        if ans is not None:
            text = ans['text']
            autograder = ans['autograder']
            a_no = ans['a_no']

        useprevious, usenew = None, None
        ## If this is a POST, write grade/comment to db.
        if cherrypy.request.method == 'POST':
            form = QuestionGradingForm()
            try:
                validated = form.to_python(data)
                grade, comment = validated['grade'], validated['comment']

                grade = grade[0]
                if 'useprevious' in data:
                    c_id = data['prevcomments']
                    save_comment_and_grade(ta, a_no, "", grade, commentid=c_id)
                else:
                    save_comment_and_grade(ta, a_no, comment, grade)
            except Exception, e:
                err = Markup(" extreme error: " + str(e) + " " + str(data))

        if ans is not None:
            existingcomment = get_existing_comment(a_no)
            existinggrade = get_existing_grade(a_no)
            prevcomments = get_previous_comments(assignment, problem)

        header=Markup('Grade an answer: (%s,%s,%s): <tt>%s</tt>'
            % (student, assignment, problem, self.g_user.user_id))

        nlines = text.count("\n")
        numbers = "\n".join(map(str, range(1, nlines+1)))
        
        focused_assignment = cherrypy.session.get('focused_assignment')
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="../assignment?a_id=%s"> \
        Assignment %s</a> > <a href="../listByStudent">List By \
        Student</a> / <a href="../listByQuestion"> List By Question</a> > \
        <b>Grade </b>' % (focused_assignment,focused_assignment))
        if err:
            ipath = err
        return template.render(source=text,
                               autograder=autograder,
                               linenumbers=numbers,
                               existingcomment=existingcomment,
                               existinggrade=existinggrade,
                               prevcomments=prevcomments,
                               student=student,
                               assignment=assignment,
                               problem=problem,
                               final_grade=final_grade,
                               ipath=ipath,
                               header=header)

def get_answer(student,assignment,question):
    """Given a student username, and assignment name, and a question name, get
    the most recent answer that matches those parameters."""

    db = mysql.DB()
    query = """
        SELECT ans.* FROM Answers ans, Questions q, Associated_with assoc, Assignment a
         WHERE  q.q_no = assoc.q_no
           AND  ans.q_no = q.q_no
           AND  assoc.s_no = a.s_no
           AND  ans.student_id = %s
           AND  a.name = %s
           AND  q.name = %s
        ORDER BY ans.a_no DESC""" 
    result = db.fetchone(query, (student,assignment,question))
    out = None
    if result:
        out = {'text':result['text'],
               'autograder':result['autograder'],
               'a_no':result['a_no']}
    db.close()
    return out

def get_existing_grade(answerid):
    """If there's a grade for this answer, pull it up."""
    db = mysql.DB()
    query = """
        SELECT sac.score FROM Score_and_comment sac
         WHERE  sac.a_no = %s"""
    result = db.fetchone(query, (answerid,))
    out = None
    if result:
        out = result['score']
    db.close()
    return out

def get_existing_comment(answerid):
    """If there's a comment stored for this answer, pull it up."""
    db = mysql.DB()
    query = """
        SELECT c.* FROM Comment c, Score_and_comment sac
         WHERE  sac.a_no = %s
           AND  sac.c_no = c.c_no
        ORDER BY c.c_no DESC""" 
    result = db.fetchone(query, (answerid,))
    out = ""
    if result:
        out = result['content']
    db.close()
    return out

def get_previous_comments(assignment,question):
    """Return a list of PreviousComment objects, where the comments are for the
    current question."""
    db = mysql.DB()
### we want all the comments that have been linked with an answer, where the
### answer is an answer to the question we're interested in.

    query = """
        SELECT DISTINCT c.* FROM Comment c, Score_and_comment sac, Answers ans,
                        Questions q, Associated_with assoc, Assignment a
         WHERE c.c_no = sac.c_no
           AND sac.a_no = ans.a_no
           AND ans.q_no = q.q_no
           AND q.q_no = assoc.q_no
           AND assoc.s_no = a.s_no
           AND a.name = %s
           AND q.name = %s
        ORDER BY c.c_no DESC""" 
    results = db.do_query(query, (assignment,question))
    out = []
    for result in results:
        out.append(PreviousComment(result['c_no'], result['content']))
    db.close()
    return out

## In the near future, we'll move to the next "relevant"
## question -- probably the same question for the next student, if possible.

def save_comment_and_grade(ta,a_no,comment,grade,commentid=None):
    """Save the comment and the grade for the current problem, for a given
    Answer."""
    comment = comment.strip()

    db = mysql.DB()
    ## relevant tables are: Score_and_comment and Comment.
    if len(comment) != 0:
        sql = "INSERT INTO Comment (content) VALUES (%s)"
        param = (comment,)
        commentid = db.do_commit(sql, param)

    if commentid:
        ## OK now insert the score and comment.
        sql = """REPLACE INTO Score_and_comment (a_no,TA_id,c_no,score)
            VALUES (%s,%s,%s,%s)"""
        param = (a_no, ta, commentid, grade)
    else:
        sql = """REPLACE INTO Score_and_comment (a_no,TA_id,score)
            VALUES (%s,%s,%s)"""
        param = (a_no, ta, grade)
    db.do_commit(sql, param)

    ## Also mark the Answer as graded.
    sql = """UPDATE Answers a SET status = "DONE"
             where a.a_no = %s
             """
    param = (a_no,)
    db.do_commit(sql, param)
    db.close()

def get_student_ids(assignment,question):
    """Return all the students for whom we have turnins for this particular
    question."""

    query = """
        SELECT DISTINCT ans.student_id
          FROM Answers ans, Questions q, Associated_with assoc, Assignment a
         WHERE ans.q_no = q.q_no
           AND q.q_no = assoc.q_no
           AND assoc.s_no = a.s_no
           AND a.name = %s
           AND q.name = %s
           ORDER BY ans.student_id ASC
           """
    db = mysql.DB()
    results = db.do_query(query, (assignment,question))
    out = []
    for result in results:
        out.append(result['student_id'])
    db.close()
    return out

def build_final_grade(student, student_ids):
    """It's sort of goofy that this object is called a FinalGrade, but it keeps
    that name for historical reasons."""
    final_grade = FinalGrade(None, student, None)
    current_index = student_ids.index(student)
    next_index = current_index + 1
    prev_index = current_index - 1
    if next_index <  len(student_ids):
        final_grade.set_next(student_ids[next_index])
    if prev_index >= 0:
        final_grade.set_prev(student_ids[prev_index])
    return final_grade
