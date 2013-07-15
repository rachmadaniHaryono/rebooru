from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'rebooru.apps.core.views.index'),
)
