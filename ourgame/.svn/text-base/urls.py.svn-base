#from django.conf.urls import patterns, include, url
#
## Uncomment the next two lines to enable the admin:
## from django.contrib import admin
## admin.autodiscover()
#
#urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'ourgame.views.home', name='home'),
#    # url(r'^ourgame/', include('ourgame.foo.urls')),
#
#    # Uncomment the admin/doc line below to enable admin documentation:
#    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#    # Uncomment the next line to enable the admin:
#    # url(r'^admin/', include(admin.site.urls)),
#)

from django.conf.urls import patterns, include, url
from maingame.views import handleRequest
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    ('^weicheck/$', handleRequest),
    url(r'^admin/', include(admin.site.urls)),
)