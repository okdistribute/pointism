from formencode import Schema, validators


class LinkForm(Schema):
    username = validators.UnicodeString(not_empty=True)
    url = validators.URL(not_empty=True, add_http=True, check_exists=False)
    title = validators.UnicodeString(not_empty=True)


class CommentForm(Schema):
    username = validators.UnicodeString(not_empty=True)
    content = validators.UnicodeString(not_empty=True)

class SemesterForm(Schema):
    term = validators.UnicodeString(not_empty=True)

class LoginForm(Schema):
    login = validators.UnicodeString(not_empty=True)
    pwd = validators.UnicodeString(not_empty=True)

class AddStudentForm(Schema):
    S_ID = validators.UnicodeString(not_empty=True)
    Name = validators.UnicodeString(not_empty=True)
    Dept = validators.UnicodeString(not_empty=True)
    E_mail = validators.UnicodeString(not_empty=True)
    Year = validators.UnicodeString(not_empty=True)

class AddTaForm(Schema):
    S_ID = validators.UnicodeString(not_empty=True)
    Name = validators.UnicodeString(not_empty=True)
    E_mail = validators.UnicodeString(not_empty=True)

class AddAssignForm(Schema):
    assmt_name = validators.UnicodeString(not_empty=True)
    questions = validators.UnicodeString(not_empty=True)

class StatisticsForm(Schema):
    assignment = validators.UnicodeString(not_empty=True)
    spilt1 = validators.UnicodeString(not_empty=True)
    output1 = validators.UnicodeString(not_empty=True)
#    assignment_all = validators.UnicodeString(not_empty=True)
#    split2 = validators.UnicodeString(not_empty=True)
#    output2 = validators.UnicodeString(not_empty=True)

class QuestionGradingForm(Schema):
    allow_extra_fields = True
    grade = validators.NotEmpty()
    comment = validators.UnicodeString(not_empty=False)
