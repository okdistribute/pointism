import operator, os, pickle, sys, time, datetime, re

## Add this directory to the Python path. It would be better, maybe, to do this
## with WSGIPythonPath in the apache config.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

sys.path.append("/opt/python-2.5/lib/python2.5/site-packages")
os.environ['PYTHON_EGG_CACHE'] = '/home/www/cache'

import cherrypy
from formencode import Invalid
from genshi.filters import HTMLFormFiller
from lib import ajax, template
from database import mysql

from model import Link, Comment, User, Student, TA, Assignment, Answer, FinalGrade
from form import LinkForm, CommentForm, SemesterForm, LoginForm, AddAssignForm, AddStudentForm, AddTaForm
from genshi.filters import HTMLFormFiller
from genshi.core import Markup


from guido_page import GuidoPage
from instructors import Instructor

class TA(GuidoPage):

    @cherrypy.expose
    @template.output('ta.html')
    def index(self):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['ta', 'final']
        self.page_for(roles)
        header = Markup('Welcome to Gudio, <tt>%s</tt>' % (self.g_user.user_id))
        ipath = 'TA: '
        return template.render(ipath = ipath, header=header, g_user=self.g_user)

    #
    # Students --> Give a grade
    #
    @cherrypy.expose
    @template.output('give_grade2student.html')
    def give_grade2student(self, **data):
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['final']
        self.page_for(roles)


        db = mysql.DB()
        sql = "SELECT * FROM Assignment WHERE term='%s'" % (self.g_term)
        results = db.do_query(sql)
        current_assignment = {}
        for row in results:
            if row['status'] == "Not Graded":
                current_assignment['a_id'] = row['s_no']
                current_assignment['a_name'] = row['name']

        cherrypy.session['current_assmt'] = current_assignment

            
        sql = "SELECT DISTINCT u.user_id, u.user_name, u.user_email FROM \
               User u, Answers a, Associated_with aw WHERE aw.q_no=a.q_no AND \
               u.user_id=a.student_id AND aw.s_no=%s ORDER BY \
               u.user_name" %(current_assignment['a_id'])
        db = mysql.DB()
        results = db.do_query(sql)
        students = []
        student_ids = []
        for row in results:
            tmp_row = {'user_id':row['user_id'],
                       'name':row['user_name'], 'email':row['user_email'],
                       'role':'student'}
            student = User(**tmp_row)
            students.append(student)
            student_ids.append(row['user_id'])
        db.close()
        cherrypy.session['student_ids'] = student_ids
        header = Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath = Markup('Final Grader: <b>Students</b><font color="grey"> > Give a grade</font>')
        return template.render(ipath=ipath , header=header,
        students=students, curr_assmt=current_assignment)


    #
    # Students --> Give a grade
    #
    @cherrypy.expose
    @template.output('give_grade.html')
    def give_grade(self, **data):
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['final']
        self.page_for(roles)

        if len(data) == 0 :
            raise cherrypy.HTTPRedirect('./give_grade2student')

        curr_user_id = data['user_id']

        current_assignment = cherrypy.session.get('current_assmt')

        f_grade = ""
        db = mysql.DB()
        if cherrypy.request.method == 'POST':
            f_grade = data['f_grade']
            sql = "REPLACE INTO Grade (TA_id,s_no,student_id,finalGrade) \
                    VALUES (%s, %s, %s, %s)"
            param = (self.g_user.user_id,current_assignment['a_id'],curr_user_id, data['f_grade'])
            db.do_commit(sql, param)

        else:
            sql = "SELECT finalGrade FROM Grade WHERE TA_id='%s' AND \
                  s_no=%s AND student_id='%s'" \
                  %(self.g_user.user_id,current_assignment['a_id'],curr_user_id)
            results = db.do_query(sql)
            for row in results:
                f_grade = row['finalGrade']

        grades = {"A":None,"B":None,"C":None,"D":None,"F":None}
        if f_grade in grades:
            grades[f_grade] = "true"

        sql = "SELECT DISTINCT q.q_no as q_no, q.name as name, sc.score as score FROM Answers a, \
               Associated_with aw, Questions q, Score_and_comment sc  \
               WHERE aw.q_no=q.q_no AND sc.a_no=a.a_no AND \
               a.q_no=q.q_no  AND a.a_no=sc.a_no AND  \
               a.student_id='%s' AND aw.s_no='%s' ORDER BY q.name" \
               %(curr_user_id, current_assignment['a_id'])
        results = db.do_query(sql)
        questions = []
        total = 0
        grade_table = {"A":5, "B":4, "C":3, "D":2, "F":1}
        for row in results:
            tmp = {'q_no':row['q_no'], 'name':row['name'], 'score':row['score']}
            total = total + grade_table[row['score']]
            questions.append(tmp)
            #total = 25
        avg = 0
        if len(questions) > 0:
            avg = total / len(questions)
        avg_score = ""
        if avg > 4 and avg <= 5:
            avg_score = "A"
        if avg > 3 and avg <= 4:
            avg_score = "B"
        if avg > 2 and avg <= 3:
            avg_score = "C"
        if avg > 1 and avg <= 2:
            avg_score = "D"
        if avg > 0 and avg <= 1:
            avg_score = "F"

        student_ids = cherrypy.session.get('student_ids')
        current_index = student_ids.index(curr_user_id)

        tmp_row = {'user_id':curr_user_id,
                   'assmt_no':current_assignment['a_name'],
                   'avg_score':avg_score}
        final_grade = FinalGrade(**tmp_row)
        next_index = current_index + 1
        prev_index = current_index - 1
        if next_index <  len(student_ids):
            final_grade.set_next(student_ids[next_index])
        if prev_index >= 0:
            final_grade.set_prev(student_ids[prev_index])
        if f_grade != "":
            final_grade.set_final_score(f_grade)

        db.close()
        header = Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath = Markup('Final Grader: <a href="./give_grade2student">Students</a> > <b>Give a grade to %s</b>' % (curr_user_id))
        return template.render(ipath=ipath , header=header,
        questions=questions, current_assmt=current_assignment,
        final_grade=final_grade, grades=grades, f_grade=f_grade)
