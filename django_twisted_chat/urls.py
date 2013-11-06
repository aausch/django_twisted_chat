from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^(/)?$', RedirectView.as_view(url='/chats/')),
     url(r'^chats/', include('chat.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
     url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)
