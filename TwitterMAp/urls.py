from django.conf.urls import patterns, include, url
from twittmap.views import my_view
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TwitterMAp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/', 'twittmap.views.my_view'),
)
