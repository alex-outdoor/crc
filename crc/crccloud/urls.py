from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_client/$', views.create_client, name='create_client'),
    url(r'^new_client/(?P<client_id>[\w\-]+)', views.edit_client, name='edit_client'),
    url(r'^list_clients/$', views.list_clients, name='list_clients'),
    url(r'^new_bid/$', views.create_bid, name='create_bid'),
    url(r'^new_bid/(?P<bid_id>[\w\-]+)', views.edit_bid, name='edit_bid'),
    url(r'^list_bids/$', views.list_bids, name='list_bids'),
]