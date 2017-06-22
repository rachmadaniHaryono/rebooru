=====
Usage
=====

To use rebooru in a project, add it to your `INSTALLED_APPS`:

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
