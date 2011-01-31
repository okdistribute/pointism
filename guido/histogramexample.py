import operator, os, pickle, sys, time, datetime, re

## Add this directory to the Python path. It would be better, maybe, to do this
## with WSGIPythonPath in the apache config.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

sys.path.append("/opt/python-2.5/lib/python2.5/site-packages")
import cherrypy
from formencode import Invalid
from genshi.filters import HTMLFormFiller
from lib import ajax, template
from database import mysql

from model import Link, Comment, User, Student, TA, Assignment, Answer
from form import QuestionGradingForm
from genshi.filters import HTMLFormFiller
from genshi.core import Markup
from guido_page import GuidoPage

class HistogramExample(GuidoPage):
    @cherrypy.expose
    @template.output('histogramex.html')
    def index(self, A=40,B=25,C=30,D=10,F=5,Z=2):
        roles = ['admin', 'ta']
        self.page_for(roles)
        self.g_user = cherrypy.session.get('g_user')
        header=Markup('Histogram example')
        ipath=Markup('histogram example')

        A,B,C,D,F,Z = map(int,[A,B,C,D,F,Z])
        timesfive = lambda x: x * 5
        awidth,bwidth,cwidth,dwidth,fwidth,zwidth = map(timesfive,[A,B,C,D,F,Z])

        return template.render(header=header, ipath=ipath,
            awidth=awidth, bwidth=bwidth, cwidth=cwidth, dwidth=dwidth,
            fwidth=fwidth, zwidth=zwidth,
            acount=A, bcount=B, ccount=C, dcount=D, fcount=F, zcount=Z)
