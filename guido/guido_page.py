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


"""In this module, we define the superclass from which other Guido page
classes inherit."""

class GuidoPage(object):
    
    class_started = "not started"
    g_term = ""
    g_role = ""
    g_home = ""
    g_user = {}
    user_table = {}
    default_term = []

    def __init__(self):
        #self.g_home = os.environ.get("REQUEST_URI")
        self.g_home = ""
        self.user_table = {'admin':'Instructor', 'ta':'TA', 'final':'TA', 'student':'Student'}
        self.default_term = ['Spring', 'Summer I', 'Summer II', 'Fall']


    #
    # role:
    # ta
    # student
    # admin (Instructor)
    #
    def page_for(self, roles):
        self.g_role = cherrypy.session.get('g_role')
        if (not (self.g_role in roles)):
            # We have to put another page to explain that you are trying
            # to access it without a proper authorization. Please talk
            # to the systems administrator to fix this problem.
            raise cherrypy.HTTPRedirect('/%s/' % (self.g_home))
            
    def has_started(self):
        if (cherrypy.session.get('class_started') != 'started'):
            raise cherrypy.HTTPRedirect('./start_class')
            
    @cherrypy.expose
    @template.output('thank.html')
    def thank(self):
        header  = 'Logout'
        ipath = ''
        self.cleanup()
        return template.render(ipath = ipath, header=header)

    def cleanup(self):
        self.class_started = ""
        self.g_role = ""
        self.g_term = ""
        self.g_user = {}
        cherrypy.session['g_user'] = None
        cherrypy.session['class_started'] = None
        cherrypy.session['g_role'] = None
        cherrypy.session['g_term'] = None
        cherrypy.session['new_assmt'] = None


    def initialize(self, username, password):

        errors = {}
        self.data = {}
        db = mysql.DB()
        self.g_role = ""
        results = db.do_query("SELECT user_id, user_name, user_email, role FROM \
        User WHERE user_id='%s' AND user_password='%s'" % (username, password))
        for row in results:
            tmp_row = {'user_id':row['user_id'], 'name':row['user_name'], 'email':row['user_email'], 'role':row['role']}
            try:
                self.g_user = User(**tmp_row)
            except Invalid, e:
                errors = e.unpack_errors()
            self.g_role = row['role']
        sql = "SELECT term "
        if(self.g_role == 'admin'):
            sql = sql + ", status "
        else:
            self.class_started = "started"
        sql = sql + "FROM %s WHERE user_id='%s'" % ( self.user_table[self.g_role], username )
        results = db.do_query(sql)
        if(len(results) > 0):
            for row in results:
                self.g_user.set_term(row['term'])
                self.g_term = row['term']
                if (self.g_role == 'admin'):
                    self.g_user.set_status(row['status'])
                    if(row['status'] == 'started'):
                        self.class_started = 'started'                
        cherrypy.session['g_user'] = self.g_user
        cherrypy.session['g_role'] = self.g_role
        cherrypy.session['g_term'] = self.g_term
        cherrypy.session['class_started'] = self.class_started
        db.close()
        return errors

    @cherrypy.expose
    @template.output('login.html')
    def login(self, **data):
        errors = {}
        self.g_role = cherrypy.session.get('g_role')
        if(self.g_role != "" and self.g_role != None):
            raise cherrypy.HTTPRedirect('./')

        if cherrypy.request.method == 'POST':
            form = LoginForm()
            try:
                data = form.to_python(data)
                self.cleanup()
                cherrypy.session['class_started'] = 'not started'

                self.initialize(data['login'], data['pwd'])


                raise cherrypy.HTTPRedirect('./')
            except Invalid, e:
                errors = e.unpack_errors()
        else:
            errors = {}

        header = 'User Login'
        # Let's disable ipath here to not show logout link.
        ipath = ''

        return template.render(errors=errors, ipath=ipath, header=header)

# Some global configuration; note that this could be moved into a
# configuration file
cherrypy.config.update({
    'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
    'tools.decode.on': True,
    'tools.trailing_slash.on': True,
    'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
    'tools.sessions.on': True,
    'tools.sessions.storage_type': "file",
    'tools.sessions.storage_path': "/home/www/sessions",
    'tools.sessions.timeout': 60,
    'tools.caching.on':False,
    'engine.autoreload_on':True
})

