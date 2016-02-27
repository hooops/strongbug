from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'strongbug.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),

    url(r'^soso',views.soso),
    url(r'^s',views.s),
    url(r'^registered',views.registered),
    url(r'^zhuce',views.zhuce),
    url(r'^login$',views.logins),
    url(r'^login_s$',views.login_view),
    url(r'^logout',views.logout_view),
    url(r'^bug/(?P<page>[\d]+)',views.bug_index),
    url(r'^add',views.handle_uploaded_files),
)
handler404 = 'views.s'