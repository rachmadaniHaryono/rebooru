from django.db import models
from rebooru.apps.accounts.models import Account

class Image(models.Model):
    # the actual pic
    file = models.FileField(upload_to='images')

    # the user account that uploaded the file
    uploader = models.ForeignKey(Account)

    def __unicode__(self):
        # the original filename. eventaully make this a hash of some sort
        return self.file.name.split('/')[-1]
