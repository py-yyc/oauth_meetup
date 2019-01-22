from django.urls import include, path

from django.contrib import admin
from django.views.generic import RedirectView

import oauth_meetup.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'polls.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path(r'', RedirectView.as_view(url='polls/')),

    path(r'polls/', include('polls.urls', namespace='polls')),
    path(r'admin/', admin.site.urls),

    path(r'oauth/', include('oauth_meetup.urls')),
    path(r'logout/', oauth_meetup.views.logout),
]
