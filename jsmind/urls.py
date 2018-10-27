from django.conf.urls import url

from . import views

app_name = 'jsmind'
urlpatterns = [
    #url(r'', views.index, name='index'),
	url(r'^owl/$', views.repoClass, name="repoclass"),
	url(r'^con/$', views.repoConn, name="repoConn"),
	url(r'^index/$', views.index, name="index"),
	url(r'^edit/$', views.edit, name="edit"),
	url(r'^viz/$', views.viz, name="viz"),
	url(r'^cal/$', views.cal, name="cal"),
	url(r'^call/$', views.call, name="call"),
	url(r'^showclass/$', views.showclass, name="showclass")
]
