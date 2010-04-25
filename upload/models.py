from django.db import models

# Create your models here.

class Submission(models.Model):
    text = models.CharField(max_length=1024 * 1024)
    upload_date = models.DateTimeField('date uploaded')
    assignment_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return "(%s, %s)" % (self.username, self.assignment_id)
