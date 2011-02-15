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

from model import Link, Comment, User, Student, TA, Assignment, Answer, Stat, Assignment_name
from form import LinkForm, CommentForm, SemesterForm, LoginForm, AddAssignForm, AddStudentForm, AddTaForm, StatisticsForm
from genshi.filters import HTMLFormFiller
from genshi.core import Markup

from guido_page import GuidoPage

class Statistics(GuidoPage):
    
    @cherrypy.expose
    @template.output('statistics.html')
    def index(self,**data):
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        
        errors={}
        a_data={}
        self.g_term = cherrypy.session.get('g_term')
        self.g_user = cherrypy.session.get('g_user')
        db = mysql.DB()
        sql = "SELECT distinct s_no, name  FROM Assignment"
        results = db.do_query(sql)

        for row in results:
           tmp_row = {'s_no':row['s_no'], 's_name':row['name']}
           assignment = Assignment_name(**tmp_row)
           a_data[assignment.s_no] = assignment

        db.close()

        assignments_all = sorted(a_data.values())

        header = 'Assignment Statistics'
        ipath = 'TA/Admin: Assignment Statistics'
        return template.render(ipath = ipath, header=header, assignments_all=assignments_all)


    @cherrypy.expose
    @template.output('show_stats_answers.html')
    def show_stats_answers(self,**data):
         self.g_user = cherrypy.session.get('g_user')
         roles = ['admin', 'ta', 'final']
         self.page_for(roles)
         header = 'Statistics Graph:'
         ipath = Markup('TA/Admin: <a href="../statistics">Assignment Statistics</a> > <b>Statistics by Answers</b>')
         self.s_data = {}
         s_data = {}
         
         sql = """
             SELECT a.q_no q_no, s.score score, q.name question,
                    count(distinct a.student_id) number
             FROM Score_and_comment s, Answers a, Assignment asg,
                  Questions q, Associated_with aw 
             WHERE  asg.name=%s
               and asg.s_no=aw.s_no
               and aw.q_no=a.q_no
               and q.q_no = a.q_no
               and a.a_no=s.a_no 
          group by s.score, a.q_no
          order by s.score, a.q_no
                """
         db = mysql.DB()
         results = db.do_query(sql, (data['assignment'],))

         for row in results:
             tmp_row = {'s_no':row['q_no'],
                        'finalGrade':row['score'], 'number':row['number']}  
              
             stat = Stat(**tmp_row)
             stat.set_year('')
             stat.question = row['question']

             s_data[stat.s_no, stat.finalGrade, stat.Year]= stat
         self.s_data = s_data

         def compareStat(s1,s2):
            if s1.question != s2.question:
                return cmp(s1.question, s2.question)
            if s1.finalGrade != s2.finalGrade:
                return cmp(s1.finalGrade, s2.finalGrade)
            return 0
         stats = sorted(self.s_data.values(),cmp=compareStat)

         return template.render(ipath = ipath, header=header, stats=stats)
      
    @cherrypy.expose
    @template.output('show_stats.html')
    def show_stats(self,**data):
        self.g_user = cherrypy.session.get('g_user')
        roles = ['admin', 'ta', 'final']
        self.page_for(roles)
        header = 'Statistical Graph'
        ipath = Markup('Admin/TA <a href="../statistics">Assignment Statistics</a> > <b>Statistics by Assignment</b>')
        self.s_data = {}
        errors = {}
        s_data = {}
     
        if (self.g_term == ""):
            self.g_term = cherrypy.session.get('g_term')
        
        s = ""
        if data['split2'] == 'year':
           s = ", s.year"

        st = " order by g.finalGrade"   
        
        if data['assignment_all'] == 'all':
           sql = "Select g.s_no s_no, g.finalGrade finalGrade, count(distinct g.student_id) number, s.year Year, \
                  5*count(distinct g.student_id) ncount FROM Student s, Grade g  where \
                  g.student_id=s.user_id group by g.finalGrade"
        else:       
           sql = "SELECT g.s_no s_no, g.finalGrade finalGrade,\
                  count(distinct g.student_id) number, s.year Year, \
                  5*count(distinct g.student_id) ncount FROM Grade g, \
                  Student s, Assignment a WHERE g.student_id=s.user_id and \
                  g.s_no=a.s_no and a.name='%s' group by g.s_no, \
                  g.finalGrade" % (data['assignment_all'])
            

        sql = sql + s + st     
    
        db = mysql.DB()
        results = db.do_query(sql)
        for row in results:
            tmp_row = {'s_no':row['s_no'], 'finalGrade':row['finalGrade'], 'number':row['number']}
            stat = Stat(**tmp_row)
            
            if data['split2'] == 'year':
               stat.set_year(row['Year'])
            else:
               stat.set_year('')
            stat.set_ncount(row['ncount'])
            s_data[stat.s_no, stat.finalGrade, stat.Year]= stat
            db.close()
        self.s_data = s_data
	    
        stats = self.s_data.values()
        
        
        return template.render(ipath=ipath, header=header, stats=stats)


