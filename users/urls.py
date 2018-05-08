from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^users/', views.register, name='register'),
]
