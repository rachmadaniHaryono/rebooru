# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from rebooru.urls import urlpatterns as rebooru_urls

urlpatterns = [
    url(r'^', include(rebooru_urls, namespace='rebooru')),
]
