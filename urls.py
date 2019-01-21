from django.urls import include, path

from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'polls.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path(r'polls/', include('polls.urls', namespace='polls')),
    path(r'admin/', admin.site.urls),
]
