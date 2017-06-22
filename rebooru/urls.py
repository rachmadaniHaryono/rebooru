# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^Image/~create/$",
        view=views.ImageCreateView.as_view(),
        name='Image_create',
    ),
    url(
        regex="^Image/(?P<pk>\d+)/~delete/$",
        view=views.ImageDeleteView.as_view(),
        name='Image_delete',
    ),
    url(
        regex="^Image/(?P<pk>\d+)/$",
        view=views.ImageDetailView.as_view(),
        name='Image_detail',
    ),
    url(
        regex="^Image/(?P<pk>\d+)/~update/$",
        view=views.ImageUpdateView.as_view(),
        name='Image_update',
    ),
    url(
        regex="^Image/$",
        view=views.ImageListView.as_view(),
        name='Image_list',
    ),
    url(
        regex="^Tag/~create/$",
        view=views.TagCreateView.as_view(),
        name='Tag_create',
    ),
    url(
        regex="^Tag/(?P<pk>\d+)/~delete/$",
        view=views.TagDeleteView.as_view(),
        name='Tag_delete',
    ),
    url(
        regex="^Tag/(?P<pk>\d+)/$",
        view=views.TagDetailView.as_view(),
        name='Tag_detail',
    ),
    url(
        regex="^Tag/(?P<pk>\d+)/~update/$",
        view=views.TagUpdateView.as_view(),
        name='Tag_update',
    ),
    url(
        regex="^Tag/$",
        view=views.TagListView.as_view(),
        name='Tag_list',
    ),
    url(
        regex="^$",
        view=views.index,
        name='index',
    )
]
