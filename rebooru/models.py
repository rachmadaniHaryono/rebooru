# -*- coding: utf-8 -*-
import os

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel


class Image(TimeStampedModel):
    file = models.FileField(upload_to='images', help_text='The actual pic.', null=True, blank=True)
    uploader = models.ForeignKey(User, help_text='The user account that uploaded the file.')
    date_uploaded = models.DateTimeField(
        auto_now_add=True, help_text='the time the file was uploaded.')
    direct_url = models.URLField(help_text='direct url alternative to file.', null=True, blank=True)

    class Meta:
        ordering = ['-date_uploaded']

    def __str__(self):
        # the original filename. eventaully make this a hash of some sort
        try:
            return os.path.basename(self.file.name)
        except AttributeError:
            return os.path.basename(self.direct_url)

    def clean(self):
        """Either direct url or file required."""
        if not self.direct_url and not self.file:
            raise ValidationError('File or direct url required.')


class Tag(TimeStampedModel):
    pass
