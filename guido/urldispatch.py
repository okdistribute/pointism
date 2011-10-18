#!/usr/bin/env python3

from bottle import route
from bottle import static_file
from bottle import request, redirect, response
from bottle import template
from bottle import abort

"""
This module handles all of the URL dispatching for Guido, mapping from URLs to
the functions that will be called in response.
"""

import reports
import grading
import frontpage
import assignment_notes
import queries
import edit_database
import csv_grades
import model
import urllib.request

guidourl = "localhost:8083"

@route('/')
def index():
    return frontpage.startpage()

                #################
################# Grading Pages #################
                #################


#######################
# Grading the problem #
#######################

# Picking the problem #

@route('/specific_problem')
def specific_post():
    return frontpage.specific_assignment()

@route('/specific_problem/pick_problem', method='POST')
def picked_assignment():
    """Called after the user has picked an assignment to grade"""
    aid = request.forms.get('assignment')
    redirect("/specific_problem/%s" % aid)
    
@route('/specific_problem/:aid')
def specific_problem_choice(aid):
    """Routed to after the user has picked an assignment to grade"""
    return frontpage.specific_problem_choice(aid)

@route('/specific_problem/:aid', method='POST')
def specific_problem_choice(aid):
    """User has picked an assignment and problem to grade."""
    problemname = request.POST.get('problem')
    first = queries.get_first_student(aid, problemname)
    redirect("/grade/%s/%s/%s" % (aid, problemname, first))

# Routing to the problem #

@route('/grade/:assignment/:problemname/:username')
def grade_problem(username, assignment, problemname):
    """Routes the user to the grading page"""
    return grading.grade(username, assignment, problemname)

@route('/grade/:assignment/:problemname/:username', method='POST')
def grade_problem(username, assignment, problemname):
    """inserts a problem grade (when there's been a post) and routes back
    to the same page"""
    grade = request.POST.get('grade')
    queries.insert_problem_grade(grade, username, assignment, problemname)
    return grading.grade(username, assignment, problemname)


#############################################################
# Submission by problem, assuming problems have been graded #
#############################################################

@route('/specific_submission')
def specific_submission():
    """Picking an assignment"""
    return frontpage.specific_submission()

@route('/specific_submission', method='POST')
def specific_submission():
    """Called after the user has picked which assignment they want to
    grade. Redirects to /grade/assignment/username"""
    aid = request.forms.get('assignment')
    first = queries.get_first_student(aid, None)
    redirect("/grade/%s/%s" % (aid, first))

@route('/grade/:assignment/:username')
def grade_submission_with_graded_problem_table(assignment, username):
    """Routes the user to the grading a submission by problem"""
    return grading.submissionbyproblem(assignment, username)

@route('/grade/:assignment/:username' , method='POST')
def grade_submission_with_graded_problem_table(assignment, username):
    """When the user posts, they are grading a whole submission."""
    return grading.submissionbyproblem(assignment, username)


################################
# Grading the whole submission #
################################

# Picking the assignment #

@route('/grade_whole/pick')
def grade_whole_pick():
    """Picking an assignment"""
    return frontpage.grade_whole()

@route('/grade_whole/pick', method='POST')
def grade_whole_pick():
    """User has picked an assignment"""
    aid = request.POST.get('assignment')
    section = request.POST.get('section')    
    first = queries.get_first_student(aid, section)
    redirect("/grade_whole/%s/%s/%s" % (aid, section, first))

# Routing to the submission #

#by section
@route('/grade_whole/:assignment/:section/:username')
def grade_whole_sections(assignment, section, username):
    """grading a whole submission by section"""
    return grading.whole_submission(assignment, username, True)

@route('/grade_whole/:assignment/:section/:username', method='POST')
def grade_whole_submissions(assignment, section, username):
    """Inserting grade and comment for a whole submission"""
    grade = request.POST.get('grade')
    queries.insert_submission_grade(grade, username, assignment)
    return grading.whole_submission(assignment, username, True)

#not by section
@route('/grade_whole/:assignment/:username')
def grade_whole_submissions(assignment, username):
    """Grading a whole submission"""
    return grading.whole_submission(assignment, username, False)

@route('/grade_whole/:assignment/:username', method='POST')
def grade_whole_submissions(assignment, username):
    """Inserting grade and comment for a whole submission"""
    grade = request.POST.get('grade')
    queries.insert_submission_grade(grade, username, assignment)
    return grading.whole_submission(assignment, username, False)


##########################
### entering a comment ###
##########################
@route('/grading/entercomment', method="GET")
def showcommentbox():
    student = request.GET.get('student');
    assignment = request.GET.get('assignment');
    problem = request.GET.get('problem');
    linenumber = request.GET.get('linenumber');
    return template("entercomment", 
                    student=student, 
                    assignment=assignment,
                    problem=problem,
                    linenumber=linenumber,
                    past_comments=list(map(lambda pair: pair[1], queries.get_all_past_comments())))

@route('/grading/entercomment', method="POST")
def insertcomment():
    comment = request.POST.get('comment')
    student = request.POST.get('student')
    assignment = request.POST.get('assignment')
    problem = request.POST.get('problem')
    linenumber = request.POST.get('linenumber')
    queries.insert_problem_comment(comment, linenumber, student, assignment, problem)
    ##this should be figured out based on the type of grading view
    redirect("/grade_whole/{0}/{1}".format(assignment, student))


@route('/grading/viewcomments', method="GET")
def viewcomment():
    """viewing a comment with delete ability"""
    student = request.GET.get('student')
    assignment = request.GET.get('assignment')
    problem = request.GET.get('problem')
    linenumber = request.GET.get('linenumber')
    report = request.GET.get('report')

    ### TODO: check to see if problem exists, if so query by problem as well
    comments = queries.get_comments_by_linenumber(student, assignment, linenumber)
    return template('viewcomments', 
                    student=student, 
                    linenumber=linenumber,
                    assignment=assignment, 
                    problem=problem, 
                    comments=comments,
                    report=report)


@route('/grading/deletecomment', method='POST')
def commentdelete():
    """deleting a comment"""
    student = request.POST.get('student')
    assignment = request.POST.get('assignment')
    text = request.POST.get('comment')
    linenumber = request.POST.get('linenumber')
    queries.delete_commentsolution(student, assignment, text, linenumber)
    redirect("/grade_whole/{0}/{1}".format(assignment, student))

                #################
################# Other Stuff #################
                #################

####################
# Viewing a report #
####################

# Picking the report #

@route('/gradingreport')
def submission_report():
    """The user is picking an assignment"""
    return frontpage.submission_report()

@route('/gradingreport/pick_username', method='POST')
def picked_assignment():
    """The user has just picked an assignment"""
    aid = request.forms.get('assignment')
    redirect("/gradingreport/%s" % aid)

@route('/gradingreport/:assignment')
def submission_report(assignment):
    """The user is picking a username"""
    return frontpage.submission_report_choice(assignment)

@route('/gradingreport/:assignment', method='POST')
def submission_report(assignment):
    """The user has just picked a username"""
    username = request.forms.get('username')
    redirect("/gradingreport/%s/%s" % (assignment, username))

# Viewing the report #
@route('/gradingreport/:assignment/:username')
def submission_report(assignment, username):
    logged_in = request.get_cookie('account', secret='some-secret-key')
    if(logged_in == username):
        return reports.submission_report(assignment, username)
    else:
        return abort(401)

@route('/login/getreport/:assignment', method='GET')
def iucas(assignment):
    #iu CAS: http://kb.iu.edu/data/atfc.html
    # get casticket from query parameters
    casticket = request.GET.get('casticket')
    # if no casticket, go to CAS, will redirect back to this site
    if not casticket:
        redirect("https://cas.iu.edu/cas/login?cassvc=IU&casurl=http://{0}/login/getreport/{1}".format(guidourl, assignment))

    validate_url = "https://cas.iu.edu/cas/validate?cassvc=IU&casticket=" + casticket
    
    # validate CAS
    f = urllib.request.urlopen(validate_url)
    s = f.read().decode()
    f.close()

    resp = s.split("\n")
    if resp[0].strip() == "yes":
        username = resp[1].strip()
        response.set_cookie("account", username, secret='some-secret-key')
        return submission_report(assignment, username)
        #redirect("/gradingreport/{0}/{1}".format(assignment, username))
    else:
        return 'login failed'
    
################################
# Editing the assignment notes #
################################

@route('/assignment_notes')
def see_assignment_notes():
    return frontpage.assignment_notes()
	
@route('/assignment_notes/edit', method='POST')
def see_assignment_notes():
    return assignment_notes.notes_edit()

@route('/assignment_notes/update/:name', method='POST')
def update_assignment_notes(name):
    return assignment_notes.notes_update(name)

############################
# Editing Database Entries #
############################

@route('/edit_database')
def splash():
    return edit_database.choice()

@route('/edit_database', method='POST')
def choosing():
    choice = request.POST.get('select')
    return edit_database.choose(choice)

@route('/edit_database_comments')
def edit_database_comments():
    fullprevcomments = queries.get_all_past_comments()
    return template("edit_database_comment",
                    prevcomments= list( map( lambda pair: model.Comment(pair[0],pair[1]), fullprevcomments)))

##################
# Error Checking #
##################

@route('/grade')
def grade():
    redirect('/specific_problem')

@route('/grade', method='POST')
def grade_post():
    redirect('/specific_problem')

@route('/none')
def unsupported():
    return template("unsupported")

##################
# Static routing #
##################

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

@route('/static/:extension/:filename')
def server_static(extension,filename):
    return static_file(filename, root='static/%s' % extension )

@route('/static/:path/:extension/:filename')
def server_static(path, extension, filename):
    return static_file(filename, root='static/%s/%s' % (path, extension) )

@route('/static/:path/:to/:extension/:filename')
def server_static(path, to, extension, filename):
    return static_file(filename, root='static/%s/%s/%s' % (path, to, extension) )

###########################
# Exporting Grades by CSV #
###########################

@route('/csv_grades')
def splash():
    return frontpage.csv_grades()

@route('/csv_grades', method='POST')
def picked_an_assignment():
    assignment = request.POST.get('assignment')
    redirect("/csv_grades/{0}".format(assignment))

@route('/csv_grades/:assignment')
def routed_to_an_assignment(assignment):
    return csv_grades.for_assignment(assignment)

#########
# Other #
#########

@route('/startpage')
def startpage():
    return frontpage.startpage()

@route('/commentdb.ajax')
def update_commentdb():
    prevcomments = grading.comments_firstline(queries.get_all_past_comments())
    return template('commentdb.ajax',
                    prevcomments=prevcomments)                    

@route('/commentedit.ajax', method='POST')
def edit_comment():
    commentid = request.POST.get('commentid')
    text = request.POST.get('text')
    queries.update_comment_text(commentid, text)
    redirect('/commentdb.ajax')

@route('/commenttext.ajax')
def getcommenttext():
    commentid = request.GET.get('commentid')
    try:
        return queries.get_comment(commentid)[1]
    except:
        return "No comment with id " + commentid    

@route('/commentdelete.ajax', method='POST')
def commentdelete():
    commentid = request.POST.get('commentid')
    queries.delete_comment(commentid)
    redirect('commentdb.ajax')

    
@route('/settings')
def settings():
    return template("settings")
