from django.conf.urls import patterns, url

from memories import views 

urlpatterns = patterns('memories.views',
    url(r'^view_near/$', 'view_near', name='view_near'),
    url(r'^view_specific/(?P<memory_id>\S+)/$', 'view_specific', name='view_specific'),
    url(r'^view_owned/$', 'view_owned', name='view_owned'),
    url(r'^edit/(?P<memory_id>\S+)/$', 'edit', name='edit'),
    url(r'^delete/(?P<memory_id>\S+)/$', 'delete', name='delete'),
    url(r'^add/', 'add', name='add'),
)
