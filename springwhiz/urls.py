from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'springwhiz.views.home', name='home'),
    # url(r'^springwhiz/', include('springwhiz.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
