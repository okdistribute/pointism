from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponse
from upload.models import Submission

# Create your views here.

def index(request):
    template = loader.get_template('upload/index.html')

    ## get the list of assignments from the database.
    assignments = "a1 a2 a3 a4".split()

    context = Context({'assignments': assignments })
    return HttpResponse(template.render(context))
