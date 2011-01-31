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

class Student(GuidoPage):

    @cherrypy.expose
    @template.output('student.html')
    def index(self):
        self.g_user = cherrypy.session.get('g_user')
        header = Markup('Welcome to Gudio, <tt>%s</tt>' % (self.g_user.user_id))
        ipath = 'Student: View your assignments'
        return template.render(ipath = ipath, header=header)

