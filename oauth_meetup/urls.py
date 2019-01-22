from django.urls import include, path

from . import views

app_name = 'meetup_oauth'
urlpatterns = [
    path('login', views.oauth, name='login'),
]
