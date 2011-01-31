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

from model import Link, Comment, User, Student, TA, Assignment, Answer
from form import LinkForm, CommentForm, SemesterForm, LoginForm, AddAssignForm, AddStudentForm, AddTaForm
from genshi.filters import HTMLFormFiller
from genshi.core import Markup


from guido_page import GuidoPage

class Instructor(GuidoPage):


    @cherrypy.expose
    @template.output('instructor.html')
    def index(self):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        header = Markup('Welcome to Guido, <tt>%s</tt>' % (self.g_user.user_id))
        ipath = 'Admin:'
        return template.render(ipath = ipath, header=header)

    #
    # start_class -> manage_class -> (student_details | ta_details)
    #
    @cherrypy.expose
    @template.output('manage_class.html')
    # def manage_class(self, **current_term):
    def manage_class(self):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        self.has_started()
        header=Markup('Admin a class (%s): <tt>%s</tt>' % (cherrypy.session.get('g_term'), self.g_user.user_id))
        ipath=Markup('Admin: <b>Manage Class</b>')
        return template.render(ipath = ipath, header=header)

    #
    # start_class -> manage_class -> (student_details | ta_details)
    #
    @cherrypy.expose
    @template.output('start_class.html')
    def start_class(self, **data):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        header = Markup('Welcome to Gudio, <tt>%s</tt>' % (self.g_user.user_id))
        ipath = Markup('Admin: <b>Start a new class</b>')
        this_year = datetime.date.today().year 
        current_terms = [ "%s %s" % (n, this_year) for n in self.default_term ]

        if cherrypy.request.method == 'POST':
            form = SemesterForm()
            try:
                data = form.to_python(data)
                self.set_semester(**data)
            except Invalid, e:
                errors = e.unpack_errors()
        else:
            errors = {}
        return template.render(errors=errors, ipath=ipath , header=header, current_terms=current_terms)

    @cherrypy.expose
    def set_semester(self, **current_term):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        cherrypy.session['class_started'] = 'started'
        db = mysql.DB()
        sql = "INSERT INTO Instructor (user_id, term, status) VALUES(%s, %s, %s)"
        param = (self.g_user.user_id, current_term['term'], cherrypy.session.get('class_started'))
        db.do_commit(sql, param)
        db.close()
        self.g_term = current_term['term']
        cherrypy.session['g_term'] = self.g_term
        self.g_user.set_term(current_term['term'])
        raise cherrypy.HTTPRedirect('./manage_class' )

    #
    # start_class -> manage_class -> (student_details | ta_details)
    #
    @cherrypy.expose
    @template.output('student_details.html')
    def student_details(self):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)

        self.s_data = {}
        errors = {}
        s_data = {}
        if(self.g_term == ""):
            self.g_term = cherrypy.session.get('g_term');
        sql = "SELECT s.*, u.user_name FROM Student s, User u WHERE \
        s.user_id=u.user_id AND s.term='%s'" % (self.g_term)
        db = mysql.DB()
        results = db.do_query(sql)
        for row in results:
            tmp_row = {'user_id':row['user_id'], 'dept':row['dept'],'year':row['year'], 'term':row['term']}
            try:
                student = Student(**tmp_row)
                student.set_name(row['user_name'])
                s_data[student.user_id] = student
            except Invalid, e:
                errors = e.unpack_errors()
        db.close()
        self.s_data = s_data

        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <b>Current Students </b>')
        students = self.s_data.values()
        return template.render(ipath = ipath, header=header, students=students)

    @cherrypy.expose
    @template.output('remove_student.html')
    def remove_student(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        sql = ""
        if cherrypy.request.method == 'POST':
            db = mysql.DB()
            sql = "DELETE FROM Student WHERE user_id=%s AND term=%s"
            param = (data['user_id'],self.g_term)
            db.do_commit(sql, param)
            db.close()
            raise cherrypy.HTTPRedirect('./student_details' )
        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <b>Current Students %s</b> %s, %s' % (sql, data['user_id'], self.g_term))
        return template.render(ipath = ipath, header=header, student=data['user_id'])

    @cherrypy.expose
    @template.output('remove_ta.html')
    def remove_ta(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        sql = ""
        if cherrypy.request.method == 'POST':
            db = mysql.DB()
            sql = "DELETE FROM TA WHERE user_id=%s AND term=%s"
            param = (data['user_id'],self.g_term)
            db.do_commit(sql, param)
            db.close()
            raise cherrypy.HTTPRedirect('./ta_details' )
        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <b>Current Students %s</b> %s, %s' % (sql, data['user_id'], self.g_term))
        return template.render(ipath = ipath, header=header, student=data['user_id'])
   

    @cherrypy.expose
    @template.output("view_assign.html")
    def view_assign(self):
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['admin', 'ta', 'final']

        if(self.g_term == ""):
            self.g_term = cherrypy.session.get('g_term');

        result = self.assignment_status(self.g_term)

        header=Markup('View an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Public: <b>View an assignment</b>')
        return template.render(ipath = ipath, header=header, results=result)
        
    @cherrypy.expose
    @template.output('finalgrader.html')
    def finalgrader(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)

        selected_assmt = data['assmt_name']
        self.get_assignment(selected_assmt)
        new_assmt = cherrypy.session.get('new_assmt')

        t_data = self.get_ta()
        new_assmt['g_term'] = self.g_term
        check_final = ""
        for ta in t_data.values():
            if ta.role == 'final':
                check_final = ta.user_id

        if cherrypy.request.method == 'POST':
            db = mysql.DB()
            if check_final != "":
                sql = "UPDATE User SET role='ta' WHERE user_id=%s"
                param = (check_final)
                db.do_commit(sql, param)
            sql = "UPDATE User SET role='final' WHERE user_id=%s"
            param = (data['user_id'])
            db.do_commit(sql, param)
            sql = "UPDATE Assignment SET status='Not Graded' WHERE s_no=%s"
            param = (new_assmt['s_no'])
            db.do_commit(sql, param)
            db.close()
            if len(data) > 0:
                check_final = data['user_id']

        for ta in t_data.values():
            if ta.user_id == check_final:
                ta.set_role("final")
                ta.set_final("true")

        new_assmt['check_final'] = check_final
        new_assmt['tas'] = t_data.values()

        header=Markup('Admin an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="add_assign">Create an assignment</a> \
        > <a href="related_assign">Related Questions</a> > <a \
        href="distribution">Distribution</a> \
         > <b>Assign Final Grader</b>')
        return template.render(ipath =ipath , header=header, new_assmt=new_assmt)

    @cherrypy.expose
    @template.output('listByQuestion.html')
    def listByQuestion(self):
        focused_assignment=cherrypy.session.get('focused_assignment')
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        sql="SELECT DISTINCT q.name from Questions q, Associated_with aw,\
        Assignment a, Answers an WHERE a.name='%s' \
        AND a.term='%s' AND a.s_no=aw.s_no AND aw.q_no=q.q_no AND\
        an.q_no=q.q_no AND an.status<>'DONE' ORDER BY q.q_no ASC" % (focused_assignment, self.g_term)
        db = mysql.DB()
        results = db.do_query(sql)
        questions = []
        for row in results:
            ques = {'name':row['name']}
            questions.append(ques)
        db.close()
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="assignment?a_id=%s"> \
        Assignment %s</a> > <b>List By \
        Question</b><font color="grey"> > Student List  > Grade </font>' % (focused_assignment,focused_assignment))
        return template.render(ipath = ipath, header=header, questions=questions, term=self.g_term, focused=focused_assignment)

    @cherrypy.expose
    @template.output('listByStudent.html')
    def listByStudent(self):

        focused_assignment = cherrypy.session.get('focused_assignment')
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        sql = "SELECT DISTINCT an.student_id from Answers an, Assignment a, Associated_with aw \
        WHERE a.name='%s' AND a.term='%s' AND a.s_no=aw.s_no AND aw.q_no=an.q_no AND an.status<>'DONE'\
        ORDER BY an.student_id ASC" % (focused_assignment, self.g_term)
        db=mysql.DB()
        results=db.do_query(sql)
        students=[]
        for row in results:
            stus = {'student_id':row['student_id']}
            students.append(stus)
        db.close()
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="assignment?a_id=%s"> \
        Assignment %s</a> > <b>List By \
        Student</b><font color="grey"> > Answer List  > Grade </font>' % (focused_assignment,focused_assignment))
        return template.render(ipath = ipath, header=header, students=students, term=self.g_term, focused=focused_assignment)


    @cherrypy.expose
    @template.output('student_answers.html')
    def student_answers(self, **data):
        cherrypy.session['focused_student']=data['s_id']
        focused_assignment = cherrypy.session.get('focused_assignment')
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        sql="SELECT DISTINCT q.name FROM Questions q, Answers an, Associated_with aw, Assignment a \
        WHERE q.q_no=an.q_no AND an.student_id='%s' AND an.status<>'DONE' AND \
        an.q_no=aw.q_no AND aw.s_no=a.s_no AND \
        a.name='%s' AND a.term='%s' ORDER BY q.q_no ASC" % (data['s_id'], focused_assignment, self.g_term)
        db=mysql.DB()
        results=db.do_query(sql)
        questions=[]
        for row in results:
            qus = {'name':row['name']}
            questions.append(qus)
        db.close()
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="assignment?a_id=%s"> \
        Assignment %s</a> > <a href=listByStudent>List By \
        Student</a> > <b> Answer List (%s)</b><font color="grey"> >\
        Grade </font>' % (focused_assignment,focused_assignment,data['s_id']))
        return template.render(ipath = ipath, header=header,\
        questions=questions, term=self.g_term,\
        focused_assignment=focused_assignment,focused_student=data['s_id'])

    @cherrypy.expose
    @template.output('question_answers.html')
    def question_answers(self, **data):
        cherrypy.session['focused_question']=data['q_id']
        focused_assignment = cherrypy.session.get('focused_assignment')
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        sql="SELECT DISTINCT an.student_id FROM Answers an, Questions q, Assignment a, Associated_with aw \
        WHERE q.name='%s' AND q.q_no=an.q_no AND an.q_no=aw.q_no AND \
        aw.s_no=a.s_no AND a.name = '%s' AND a.term='%s' AND\
        an.status<>'DONE' ORDER BY an.student_id ASC" % (data['q_id'], focused_assignment, self.g_term)
        db=mysql.DB()
        results=db.do_query(sql)
        s_answers=[]
        for row in results:
            stud = {'student_id':row['student_id']}
            s_answers.append(stud)
        db.close()
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="assignment?a_id=%s"> \
        Assignment %s</a> > <a href=listByQuestion>List By \
        Question</a> > <b> Student List (Question %s)</b><font color="grey"> > \
        Grade </font>' % (focused_assignment,focused_assignment,data['q_id']))
        return template.render(ipath = ipath, header=header,\
        answers=s_answers, term=self.g_term,\
        focused_assignment=focused_assignment,focused_question=data['q_id'])


    #
    # add_assign -> related_assign -> distribution -> finalgrader 
    #
    @cherrypy.expose
    @template.output('distribution.html')
    def distribution(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)

        selected_grader = {}
        if len(data) == 0:
            raise cherrypy.HTTPRedirect('./add_assign')

        selected_assmt = data['assmt_name']
        self.get_assignment(selected_assmt)
        new_assmt = cherrypy.session.get('new_assmt')
        t_data = self.get_ta()
        new_assmt['tas'] = t_data.values()
        new_assmt['g_term'] = self.g_term
        questions = new_assmt['questions']  # Questions of the selected assignment
        
        if cherrypy.request.method == 'POST':
            db = mysql.DB()

            myList = questions.keys()
            myList = list(set(myList))
            q_list = self.make_string(myList)
            # Clean the Distributed table 
            sql = "DELETE FROM Distributed WHERE q_no IN (%s)"
            param = (q_list)
            db.do_commit(sql, param)

            g = re.compile("grader")
            for key, value in sorted(data.items()):
                if g.match(key):
                    sql = "INSERT INTO Distributed (q_no, instructor_id, TA_id) \
                           VALUES(%s, %s, %s)"
                    q_no = key.replace('grader_', '')
                    param = (q_no, self.g_user.user_id, key)
                    db.do_commit(sql, param)
                    selected = {}
                    for ta in new_assmt['tas']:
                        if ta.user_id == value:
                            selected[ta] = "true"
                        else:
                            selected[ta] =  None
                    selected_grader[q_no] = selected
            new_assmt["selected_grader"] = selected_grader
            db.close()
            raise cherrypy.HTTPRedirect('./finalgrader' )

        if len(data) == 0 and cherrypy.session.get('new_assmt') == None :
            raise cherrypy.HTTPRedirect('./add_assign' )
            

        header=Markup('Admin an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="add_assign">Create an assignment</a> \
        > <a href="related_assign">Related Questions</a> > \
        <b>Distribution</b> \
        <font color="grey"> > Assign Final Grader </font>')
        return template.render(ipath = ipath, header=header, new_assmt=new_assmt)


    def assignment_status(self, g_term):    
        # Total number of answers in each assingment
        sql1 = "SELECT count(*) AS count, ag.name FROM Answers a, Assignment ag, Associated_with ac WHERE \
        a.q_no = ac.q_no AND ag.s_no = ac.s_no AND ag.term='%s' GROUP BY ag.name" % (self.g_term)
        db = mysql.DB()
        results1 = db.do_query(sql1)
        answers = []
        for row in results1:
            assmt= {'name':row['name'], 'count':row['count']}
            answers.append(assmt)

        # Total number of questions in each assingment
        sql1 = "SELECT count(*) AS count, ag.name FROM Assignment ag, Associated_with ac WHERE \
         ag.s_no = ac.s_no AND ag.term='%s' GROUP BY ag.name" % (self.g_term)
        db = mysql.DB()
        results1 = db.do_query(sql1)
        questions = []
        for row in results1:
            qst= {'name':row['name'], 'count':row['count']}
            questions.append(qst)

        # Total number of graded answers in each assingment
        sql2 = "SELECT count(*) AS count, ag.name FROM Answers a, Assignment ag, Associated_with ac WHERE \
        a.q_no = ac.q_no AND ag.s_no = ac.s_no AND ag.term='%s' AND a.status='DONE' GROUP BY ag.name" % (self.g_term)
        db = mysql.DB()
        results2 = db.do_query(sql2)
        graded_answers = []
        for row in results2:
            graded = {'name':row['name'], 'count':row['count']}                
            graded_answers.append(graded)
        db.close()

        #sql2 = "SELECT count(*) AS count, ag.name FROM Grade g, Assignment ag WHERE \
        #ag.s_no = g.s_no AND ag.term='%s' GROUP BY ag.name" % (self.g_term)
        #db = mysql.DB()
        #results2 = db.do_query(sql2)
        #graded_answers = []
        #for row in results2:
        #    graded = {'name':row['name'], 'count':row['count']}                
        #    graded_answers.append(graded)
        #db.close()

        if len(questions) > len(answers):
            i = 0
            for question in questions:
                if i >= len(answers):
                    answer = {'name':question['name'], 'count':0}
                    answers.append(answer)
                if i >= len(graded_answers):
                    graded_answer = {'name':question['name'], 'count':0}
                    graded_answers.append(graded_answer)
                i = i + 1

        return map (self.check_graded, answers, graded_answers)

    def check_graded (self, x, y):
       a = x['count'] # total answers in each assignment
       b = y['count'] # graded answers in each assignment
       c = {}
       c['name'] = x['name']
       if a == b and a != 0 :
           c['status'] = "Graded"
       else:
           c['status'] = Markup("<a href=\"assignment?a_id=%s\"><font color=\"red\"><b>Not graded (%s/%s)</b></font></a>" % (c['name'], b, a))
       c['count'] = a
       return c

    @cherrypy.expose
    @template.output('assignment.html')
    def assignment(self,**data):
        cherrypy.session['focused_assignment']=data['a_id']
        self.g_user = cherrypy.session.get('g_user')
        self.g_term = cherrypy.session.get('g_term')
        roles =['admin', 'ta', 'final']
        self.page_for(roles)
        header=Markup('Admin an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > \
        <b>Assignment %s</b><font color="grey">  > List By Student / \
        List By Question > Grade </font>' % (data['a_id']))
        return template.render(ipath =ipath , header=header, focused_assignment=data['a_id'], term=self.g_term)

    @cherrypy.expose
    @template.output('assignment_list.html')
    def assignment_list(self):
	
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        self.has_started()

        if(self.g_term == ""):
            self.g_term = cherrypy.session.get('g_term');

        result = self.assignment_status(self.g_term)

        header=Markup('Admin an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <b>Grade an assignment</b>')
        return template.render(ipath = ipath, header=header, results=result)

    #
    # add_assign -> related_assign -> distribution -> finalgrader 
    #
    @cherrypy.expose
    @template.output('add_assign.html')
    def add_assign(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        self.has_started()

        errors = {}
        if cherrypy.request.method == 'POST':
            form = AddAssignForm()
            try:
                data = form.to_python(data)
                self.set_assignment(**data)
                raise cherrypy.HTTPRedirect('./related_assign')
            except Invalid, e:
                errors = e.unpack_errors()

        results = self.assignment_status(self.g_term)
        current_assignment = ""
        check_first = 0
        verb = "is"
        new_assmts = []
        for result in results:
            if result['count'] == 0:
                if check_first > 0:
                    verb = "are"
                    current_assignment += ", "
                current_assignment += result['name']
                new_assmts.append(result['name'])
                check_first = check_first + 1
        message = {'msg':Markup("The current assignment(s) (<font \
        color=\"red\">%s</font>) %s not published yet." % (current_assignment, verb)),
        'term':self.g_term,
        'related_qs':new_assmts}

        header=Markup('Admin an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <b>Create an assignment</b> <font color="grey"> >\
        Related \
        Questions > Distribution > Assign Final Grader </font>')
        return template.render(errors=errors, ipath =ipath , header=header, message=message)

    def set_assignment(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        db = mysql.DB()
        sql = "INSERT INTO Assignment (name, term) VALUES(%s, %s)"
        param = (data['assmt_name'], self.g_term)
        db.do_commit(sql, param)
        sql = "SELECT s_no FROM Assignment WHERE name='%s' AND \
        term='%s'" % (data['assmt_name'], self.g_term)
        assmt_no = ""
        results = db.do_query(sql)
        for row in results:
            assmt_no = row['s_no']

        questions = data['questions'].replace(' ', '').split(',')
        for question in questions:
            sql = "INSERT INTO Questions (name, create_date) VALUES (%s, now())"
            param = (question)
            db.do_commit(sql, param)
            sql = "INSERT INTO Associated_with (q_no, s_no) SELECT \
            q_no, %s FROM Questions WHERE name=%s AND create_date=current_date()"
            param = (assmt_no, question)
            db.do_commit(sql, param)
        db.close()
        self.get_assignment(data['assmt_name'])


    def get_assignment(self, assmt_name):
        self.g_term = cherrypy.session.get('g_term')
        if assmt_name == "" or assmt_name == None:
            results = self.assignment_status(self.g_term)
            for result in results:
                if result['count'] == 0:
                    assmt_name = result['name']
        db = mysql.DB()
        sql = "SELECT s_no FROM Assignment WHERE name='%s' AND \
        term='%s'" % (assmt_name, self.g_term)
        assmt_no = ""
        results = db.do_query(sql)
        for row in results:
            assmt_no = row['s_no']
        sql = "SELECT ag.*, q.name FROM Associated_with ag,  \
        Questions q WHERE q.q_no=ag.q_no AND ag.s_no=%s" % (assmt_no)
        results = db.do_query(sql)
        questions = {};
        for row in results:
            questions[row['q_no']] = row['name']
        q_list = "( "+ ','.join(str(n) for n in questions.keys()) + " )"
        sql = "SELECT * FROM Related_q WHERE q_no IN %s" % (q_list)
       
        results = db.do_query(sql)
        selected_group = {};
        for row in results:
            selected_group[row['q_no']] = row['group_name']

        selected_grader = {};
        t_data = self.get_ta()
        tas = t_data.values()
        default_group = ['A','B','C','D','E']
        related_questions = {}
        for q_no, q_name in sorted(questions.items()):
            related_group = {};
            for g in default_group:
                str2 = re.compile(g)
                if q_no in selected_group.keys() and str2.match(selected_group[q_no]):
                    related_group[g] = "true"
                else:
                    related_group[g] = None
            related_questions[q_no] = related_group

            selected = {}
            for ta in tas:
                selected[ta] = None
            selected_grader[q_no] = selected        


        distributed = {}
        sql = "SELECT * FROM Distributed WHERE q_no IN %s" % (q_list)
        results = db.do_query(sql)
        for row in results:
            selected = {}
            for ta in tas:
                if ta.user_id == row['TA_id']:
                    selected[ta] = "true"
                else:
                    selected[ta] = None
            selected_grader[row['q_no']] = selected        
            distributed[row['q_no']] = row['TA_id']


        db.close()
        cherrypy.session['new_assmt'] = {'name':assmt_name,
                                         's_no':assmt_no,
                                         'count':len(questions),
                                         'questions':questions,
                                         'selected_group':selected_group,
                                         'related_questions':related_questions,
                                         'distributed':distributed,
                                         'selected_grader':selected_grader}

    #
    # start_class -> manage_class -> (student_details | ta_details)
    #
    @cherrypy.expose
    @template.output('ta_details.html')
    def ta_details(self):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)

        self.t_data = {}
        self.t_data = self.get_ta()

        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <b>Current TAs </b>')
        tas = self.t_data.values()
        return template.render(ipath = ipath, header=header, tas=tas)

    def get_ta(self):
        t_data = {}
        sql = "SELECT t.*, u.role, u.user_name FROM TA t, User u WHERE \
        t.user_id=u.user_id AND t.term='%s'" % (self.g_term)
        db = mysql.DB()
        results = db.do_query(sql)
        for row in results:
            tmp_row = {'user_id':row['user_id'], 'term':row['term']}
            ta = TA(**tmp_row)
            ta.set_name(row['user_name'])
            ta.set_role(row['role'])
            t_data[ta.user_id] = ta
        db.close()
        return t_data


    @cherrypy.expose
    @template.output('add_student.html')
    def add_student(self, **data):
        errors={}
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        self.page_for(roles)
        sql = ""
        if cherrypy.request.method == 'POST':
            form = AddStudentForm()
            try:
                data = form.to_python(data)
                db = mysql.DB()
                sql = "INSERT INTO Student VALUES ("
                sql += "%s, %s, %s, %s)"
                param=(data['S_ID'],data['Dept'],data['Year'], 'Spring 2010')
                db.do_commit(sql, param)
                sql = "INSERT INTO User (user_id, user_password, user_email, user_name, role) "
                sql += "SELECT %s, '111', %s, %s, 'student' "
                sql += "FROM User WHERE NOT EXISTS (SELECT * FROM User WHERE User.user_id = %s)"
                param=(data['S_ID'],data['E_mail'],data['Name'],data['S_ID'])
                db.do_commit(sql, param)
                db.close
                raise cherrypy.HTTPRedirect('./student_details' )
            except Invalid, e:
                errors = e.unpack_errors()
       
        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <a href = "student_details">Current Students</a> ><b>Add Student</b>')
        return template.render(errors = errors, ipath = ipath, header=header)

    @cherrypy.expose
    @template.output('add_ta.html')
    def add_ta(self, **data):
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin']
        errors={}
        self.page_for(roles)
        sql = ""
        if cherrypy.request.method == 'POST':
            form = AddTaForm()
            try:
                data = form.to_python(data)
                db = mysql.DB()
                sql = "INSERT INTO TA VALUES ("
                sql += "%s, %s)"
                param=(data['S_ID'], 'Spring 2010')
                db.do_commit(sql, param)
                sql = "INSERT INTO User (user_id, user_password, user_email, user_name, role) "
                sql += "SELECT %s, '111', %s, %s, 'ta' "
                sql += "FROM User WHERE NOT EXISTS (SELECT * FROM User WHERE User.user_id = %s)"
                param=(data['S_ID'],data['E_mail'],data['Name'],data['S_ID'])
                db.do_commit(sql, param)
                db.close
                raise cherrypy.HTTPRedirect('./ta_details' )
            except Invalid, e:
                errors = e.unpack_errors()
        header=Markup('Admin a class (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin: <a href="manage_class">Manage Class</a> > \
        <a href = "ta_details">Current Students</a> ><b>Add TA</b>')
        return template.render(errors=errors, ipath=ipath, header=header)
   
# Some global configuration; note that this could be moved into a
# configuration file
cherrypy.config.update({
    'tools.caching.on':False,
    'engine.autoreload_on':False
})

