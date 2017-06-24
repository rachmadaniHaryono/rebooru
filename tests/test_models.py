#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_rebooru
------------

Tests for `rebooru` models module.
"""

from django.test import TestCase

from rebooru import models


class TestRebooru(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass


def test_save_direct_url_twice():
    user = User(username='name')
    user.save()
    img = models.Image(direct_url='http://i.imgur.com/RBqNZki.jpg', uploader=user)
    img.save()
    img2 = models.Image(direct_url='http://i.imgur.com/RBqNZki.jpg', uploader=user)
    with pytest.raises(ValidationError):
        img2.save()
