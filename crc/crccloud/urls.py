from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.create, name='create'),
]