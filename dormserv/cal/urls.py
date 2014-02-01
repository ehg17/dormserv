from django.conf.urls import patterns, url
from cal import views

urlpatterns = patterns('',
	url(r'^$', views.display_calendar, name='display_calendar'),
	url(r'^(?P<entry_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<entry_id>\d+)/detail/validate_purchase', views.validate_purchase, name='validate_purchase'),
	url(r'^(?P<entry_id>\d+)/detail', views.detail, name='detail2'),
	url(r'^profile', views.profile, name='profile'),
    )