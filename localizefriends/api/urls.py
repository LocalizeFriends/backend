from django.conf.urls import url

from . import views

app_name = 'urls'
urlpatterns = [
    url(r'^location$', views.update_location, name='update_location'),
    url(r'^$', views.index, name='index'),
]
