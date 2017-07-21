# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
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

    parsed_urls = list(parse_url(url))
    img_urls = list(filter_image_url(parsed_urls))
    if depth == 1:
        non_img_urls = [x for x in parsed_urls if x not in img_urls]
        purls_d1 = list(map(parse_url, non_img_urls))
        [img_urls.extend(filter_image_url(list(x))) for x in purls_d1]

    user, _ = User.objects.get_or_create(username='default_user', password='1234')
    url_tag = url.split(':', 1)
    tag = Tag.objects.get_or_create(name=url_tag[1], namespace=[0])
    img_object = []
    for img_url in img_urls:
        im, _ = Image.objects.get_or_create(uploader=user, direct_url=img_url)
        img_object.append(im)

    return render_to_response('rebooru/index.html', {'images': img_object})
