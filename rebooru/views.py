# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse, urljoin

import requests
import django
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from yapsy.PluginManager import PluginManager
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Image,
    ParseResult,
    QueryModel,
    Tag,
)
from . import plugin


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


class ParseResultListView(ListView):

    model = ParseResult


def filter_image_url(urls):
    for url in urls:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
        if ext in ('.jpg', '.png', 'jpeg'):
            yield url


def parse_url(url):
    """parse url and return images url."""
    html_soup = BeautifulSoup(requests.get(url).content, "html.parser")
    tag_hrefs = []
    for a_tag in html_soup.select('a'):
        href = a_tag.attrs.get('href', None)
        if a_tag.select('img') and href is not None:
            tag_hrefs.append(href)
    for href in tag_hrefs:
        if href.startswith('/'):
            yield urljoin(url, href)

def index(request):
    """Just displays some images

    .. todo:: pagination on object.
    .. todo:: explain url query.
    .. todo:: generic parser.
    """
    query = request.GET.get('q', None)
    if query is None:
        context = {
            'images': Image.objects.all()[:20],
        }
        return render_to_response('rebooru/index.html', context)


    query_parts = query.split(' ')
    url = next((x for x in query_parts if x.startswith(('http:', 'https:'))), None)
    depth = next((x for x in query_parts if x.startswith('depth:')), None)


    if url is None:
        return render_to_response('rebooru/index.html', {'images': []})
    if depth is not None:
        depth = int(depth.split(':', 1)[1])

    parse_results = list(plugin.parse_url(url))

    user, _ = User.objects.get_or_create(username='default_user', password='1234')
    url_tag = url.split(':', 1)
    tag, _ = Tag.objects.get_or_create(name=url_tag[1], namespace=[0])
    img_object = []
    query_model, _ = QueryModel.objects.get_or_create(query=query)
    for item in parse_results:
        item['query'] = query_model
        ParseResult.objects.get_or_create(**item)
        if item['type'] != ParseResult.TYPE_IMAGE:
            continue
        img_url = item['url']
        im, _ = Image.objects.get_or_create(uploader=user, direct_url=img_url)
        im.tags.add(tag)
        try:
            im.save()
        except django.core.exceptions.ValidationError:
            pass
        img_object.append(im)

    return render_to_response('rebooru/index.html', {'images': img_object})
