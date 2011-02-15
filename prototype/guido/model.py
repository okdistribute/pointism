from datetime import datetime

# Collection of the main classes of guido
class Assignment_name(object):
    def __init__(self, s_no, s_name):
        self.s_no = s_no
        self.s_name = s_name

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, s_no)

class Assignment(object):

    def __init__(self, username, a_no):
        self.username = username
        self.a_no = a_no
        self.answers = []
        # We need to set finalgrader and final_grade later 
        self.finalgrader = None
        self.final_grade = None

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.username)

    def add_answer(self, q_no, grade, comment):
        answer = Answer(q_no, grade, comment)
        self.answers.append(answer)
        return answer

    def set_finalgrader(self, finalgrader):
        self.finalgrader = finalgrader

    def set_final_grade(self, final_grade):
        self.final_grade = final_grade

class Answer(object):

    def __init__(self, q_no, grade, comment):
        self.q_no = q_no
        self.grade = grade
        self.comment = comment

    def __repr__(self):
        return '<%s of the question %r>' % (type(self).__name__, self.q_no)

class User(object):

    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.term = None
        self.status = None

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.user_id)

    def set_term(self, term):
        self.term = term

    # Maybe we don't need it any more because role will take care of it.
    def set_finalgrader(self, finalgrader):
        self.finalgrader = finalgrader

    def set_status(self, status):
        self.status = status

    def is_final(self):
        return self.role == "final"


class Student(object):
    def __init__(self, user_id, dept, year, term):
        self.user_id = user_id
        self.term = term
        # We need to set dept and year if necessary
        self.dept = dept
        self.year = year

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.user_id)

    def set_term(self, term):
        self.term = term

    def set_name(self, name):
        self.name = name

    def set_student(self, dept, year):
        self.dept = dept
        self.year = year

class Stat(object):
    
    def __init__(self, s_no, finalGrade, number):
        self.s_no = s_no
        self.finalGrade = finalGrade
        self.number = number

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.s_no) 
    
    def set_year(self, Year):
        self.Year = Year

    def set_ncount(self,ncount):
        self.ncount = ncount

class TA(object):
    def __init__(self, user_id, term):
        self.user_id = user_id
        self.term = term
        self.final = None


    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.user_id)

    def set_role(self, role):
        self.role = role 

    def set_name(self, name):
        self.name = name

    def set_final(self, final):
        self.final = final

class FinalGrade(object):
    def __init__(self, assmt_no, user_id, avg_score):
        self.user_id = user_id
        self.assmt_no = assmt_no
        self.avg_score = avg_score
        self.final_score = None
        self.next_student = None
        self.prev_student = None

    def __repr__(self):
        return '<%s of %r>' % (type(self).__name__, self.assmt_no)

    def set_final_score(self, final_score):
        self.final_score = final_score

    def set_next(self, user_id):
        self.next_student = user_id 

    def get_next(self):
        return self.next_student

    def set_prev(self, user_id):
        self.prev_student = user_id 

    def get_prev(self):
        return self.prev_student

    

class Link(object):

    def __init__(self, username, url, title):
        self.username = username
        self.url = url
        self.title = title
        self.time = datetime.utcnow()
        self.id = hex(hash(tuple([username, url, title, self.time])))[2:]
        self.comments = []

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.title)

    def add_comment(self, username, content):
        comment = Comment(username, content)
        self.comments.append(comment)
        return comment

class Comment(object):
    """Example from the Genshi tutorial."""
    def __init__(self, username, content):
        self.username = username
        self.content = content
        self.time = datetime.utcnow()

    def __repr__(self):
        return '<%s by %r>' % (type(self).__name__, self.username)

class PreviousComment(object):
    """Quick representation of comments that have been stored in the database
    previously."""
    def __init__(self, c_no, content):
        self.c_no = c_no
        self.content = content
        self.firstline = ""
        if len(content) > 0:
            self.firstline = content.split("\n")[0]
        else:
            self.firstline = "(empty)"
