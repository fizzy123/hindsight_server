from django.conf.urls import patterns, url

from users import views 

urlpatterns = patterns('users.views',
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),
    url(r'^create/$', 'create', name='create'),
    url(r'^verify/$', 'verify', name='verify'),
    url(r'^verify_email/(?P<key>\S+)/$', 'verify_email', name='verify_email'),
    url(r'^provide_csrf/$', 'provide_csrf', name='provide_csrf'),
)
