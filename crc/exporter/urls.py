from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bid/(?P<bid_id>\w+|)', views.export_bid, name='export_bid'),
    url(r'^pdf', views.pdf_bid, name='pdf'),
]