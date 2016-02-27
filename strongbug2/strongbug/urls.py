from django.conf.urls import patterns, include, url
#from django.contrib import admin
from strongbug_main import urls
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'strongbug.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include(urls)),
)
