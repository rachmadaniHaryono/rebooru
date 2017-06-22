=============================
rebooru
=============================

.. image:: https://badge.fury.io/py/rebooru.svg
    :target: https://badge.fury.io/py/rebooru

.. image:: https://travis-ci.org/rachmadaniHaryono/rebooru.svg?branch=master
    :target: https://travis-ci.org/rachmadaniHaryono/rebooru

.. image:: https://codecov.io/gh/rachmadaniHaryono/rebooru/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rachmadaniHaryono/rebooru

A django-based booru with complex tagging and searching

Documentation
-------------

The full documentation is at https://rebooru.readthedocs.io.

This is going to eventually, hopefully, be a django booru with a deep tagging and search system.

Quickstart
----------

If you're installing this for some reason, see the requirements file.

Gunicorn config is included because @xephero use it.

note for gunicorn config:the SECRET_KEY setting will auto-generate the first time you run it,
and get saved to a file and imported from that in the future.
This is to avoid multiple servers using the same key,
or revealing it accidentally (the file is in .gitignore).

Install rebooru::

    pip install rebooru

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rebooru.apps.RebooruConfig',
        ...
    )

Add rebooru's URL patterns:

.. code-block:: python

    from rebooru import urls as rebooru_urls


    urlpatterns = [
        ...
        url(r'^', include(rebooru_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
