from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_client/(?P<client_id>\w+|)', views.create_client, name='new_client'),
    url(r'^list_clients/$', views.list_clients, name='list_clients'),
    url(r'^new_bid/(?P<bid_id>\w+|)', views.create_bid, name='create_bid'),
    url(r'^list_bids/$', views.list_bids, name='list_bids'),
]