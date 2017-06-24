from django.contrib import admin
from rebooru import models

admin.site.register(models.Image)
admin.site.register(models.Tag)
