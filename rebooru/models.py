# -*- coding: utf-8 -*-
import os
from urllib.parse import unquote

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ValidationError, ObjectDoesNotExist

from model_utils.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=128)
    namespace = models.CharField(max_length=128)
    creator = models.BooleanField(default=False)
    series = models.BooleanField(default=False)
    character = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.namespace == 'creator':
            self.creator = True
        elif self.namespace == 'series':
            self.series = True
        elif self.namespace == 'character':
            self.character = True
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ImageManager(models.Manager):

    def create_image(self, **kwargs):
        image = self.create(**kwargs)
        return image

class Image(TimeStampedModel):
    RATING_UNKNOWN = -1
    RATING_SAFE = 0
    RATING_QUESTIONABLE = 1
    RATING_EXPLICIT = 2
    RATING_CHOICES = (
        (RATING_UNKNOWN, 'unknown'),
        (RATING_SAFE, 'safe'),
        (RATING_QUESTIONABLE, 'questionable'),
        (RATING_EXPLICIT, 'explicit'),
    )
    file = models.FileField(upload_to='images', help_text='The actual pic.', null=True, blank=True)
    uploader = models.ForeignKey(User, help_text='The user account that uploaded the file.')
    date_uploaded = models.DateTimeField(
        auto_now_add=True, help_text='the time the file was uploaded.')
    direct_url = models.URLField(help_text='direct url alternative to file.', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=RATING_UNKNOWN, choices=RATING_CHOICES)

    objects = ImageManager()

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

    def save(self, **kwargs):
        if self.direct_url:
            direct_url_already_exist_msg = 'Image with that url already exist.'
            try:
                Image.objects.get(direct_url=self.direct_url)
                raise ValidationError(direct_url_already_exist_msg)
            except MultipleObjectsReturned:
                raise ValidationError(direct_url_already_exist_msg)
            except ObjectDoesNotExist:
                pass
        if(self.rating > 2):
            raise ValidationError("rating must be safe, questionable, or explicit.")
        else:
            super().save(**kwargs)


class QueryModel(TimeStampedModel):
    query = models.CharField(max_length=255)


class ParseResult(TimeStampedModel):
    TYPE_UNKNOWN = -1
    TYPE_PAGE = 0
    TYPE_IMAGE = 1
    TYPE_VIDEO = 2
    TYPE_CHOICES = (
        (TYPE_UNKNOWN, 'unknown'),
        (TYPE_PAGE, 'page'),
        (TYPE_IMAGE, 'image'),
        (TYPE_VIDEO, 'video'),
    )
    url = models.URLField(help_text='URL result')
    source_url = models.URLField(help_text='Source url')
    type = models.IntegerField(default=TYPE_UNKNOWN, choices=TYPE_CHOICES)
    query = models.ForeignKey(QueryModel)

    def type_verbose(self):
        return dict(ParseResult.TYPE_CHOICES)[self.type]

    def url_entry_on_table(self):
        unquoted_url = unquote(self.url)
        return unquoted_url.split('://', 1)[1]
