from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dormserv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('users.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('users.urls')),
	url(r'^cal/', include('cal.urls')),
)
