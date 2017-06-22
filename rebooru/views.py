# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Image,
    Tag,
)


class ImageCreateView(CreateView):

    model = Image


class ImageDeleteView(DeleteView):

    model = Image


class ImageDetailView(DetailView):

    model = Image


class ImageUpdateView(UpdateView):

    model = Image


class ImageListView(ListView):

    model = Image


class TagCreateView(CreateView):

    model = Tag


class TagDeleteView(DeleteView):

    model = Tag


class TagDetailView(DetailView):

    model = Tag


class TagUpdateView(UpdateView):

    model = Tag


class TagListView(ListView):

    model = Tag

