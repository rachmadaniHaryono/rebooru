#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_rebooru
------------

Tests for `rebooru` models module.
"""

from django.test import TestCase
import pytest

from rebooru import models


class TestRebooru(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass

@pytest.mark.django_db(transaction=True)
def test_save():
    user = models.User(username='name')
    user.save()
    img = models.Image(direct_url='http://i.imgur.com/RBqNZki.jpg', uploader=user)
    img.save()
