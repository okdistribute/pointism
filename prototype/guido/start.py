#!/opt/python/bin/python

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

from model import User, Student, TA, Assignment, Answer
from form import LinkForm, CommentForm, SemesterForm, LoginForm, AddAssignForm, AddStudentForm, AddTaForm
from genshi.filters import HTMLFormFiller
from genshi.core import Markup

from guido_page import GuidoPage

class Root(GuidoPage):

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        self.g_role = cherrypy.session.get('g_role')
        if(self.g_role == "" or self.g_role == None):
            raise cherrypy.HTTPRedirect('./login')
        if(self.g_role == 'admin'):
            raise cherrypy.HTTPRedirect('./instructor')
        if(self.g_role == 'ta' or self.g_role =='final'):
            raise cherrypy.HTTPRedirect('./ta')
        if(self.g_role == 'student'):
            raise cherrypy.HTTPRedirect('./student')


    @cherrypy.expose
    @template.output('archive.html')
    def archive(self):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin', 'ta']
        self.page_for(roles)
        header=Markup('Admin assignment archives: <tt>%s</tt>' % (self.g_user.user_id))
        ipath=Markup('Admin: <font color="grey">Archive/Load old assignments</font>')
        return template.render(ipath =ipath , header=header)

    @cherrypy.expose
    @template.output('feedback.html')
    def feedback(self):
        header = 'View the comments of your A3'
        ipath = 'Student: Your graded assignment'
        return template.render(ipath =ipath , header=header)

    @cherrypy.expose
    @template.output('load.html')
    def load(self):
        roles = ['admin', 'ta']
        self.page_for(roles)
        header=Markup('Load old archives: <tt>%s</tt>' % (self.g_user.user_id))
        ipath=Markup('Admin: <b>Archive/Load old assignments</b>')
        return template.render(ipath = ipath, header=header)


    @cherrypy.expose
    @template.output('searchresults.html')
    def searchresults(self):
        header = Markup('Welcome to Gudio, <tt>%s</tt>' % (self.g_user.user_id))
        ipath = 'Student: Assignments with code or comments matching "fac"...'
        return template.render(ipath = ipath, header=header)


    @cherrypy.expose
    @template.output('selected_student.html')
    def selected_student(self):
        roles = ['admin','ta']
        self.page_for(roles)
        header=Markup('Grade an assignment (%s): <tt>%s</tt>' % (self.g_term, self.g_user.user_id))
        ipath=Markup('Admin/TA: <a href="assignment_list">Grade an \
        assignment</a> > <a href="assignment3"> \
        Assignment 3</a> > <a href="listByStudent">List By \
        Student</a> > <b>Student 1</b> <font color="grey"> > Grade \
        </font>')
        return template.render(ipath = ipath, header=header)

        
from histogramexample import HistogramExample
from gradingpage import GradingPage
from instructors import Instructor
from statistics import Statistics
from ta import TA
from student import Student
from codesearch import CodeSearch

#g_home = os.environ.get("REQUEST_URI")
g_home = "guido"
root = Root()
root.instructor = Instructor()
root.instructor.grading = GradingPage()
root.instructor.statistics = Statistics()
root.ta = TA()
root.ta.grading = GradingPage()
root.ta.statistics = Statistics()
root.student = Student()
#root.statistics = Statistics()
root.grading = GradingPage()
root.histogram = HistogramExample()
root.codesearch = CodeSearch()

application = cherrypy.Application(root, '/%s/' % (g_home), {
    '/media': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static'
    }
})
