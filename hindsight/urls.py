from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^users/',  include('users.urls', namespace='users')),
    url(r'^memories/',  include('memories.urls', namespace='memories'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
