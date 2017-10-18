# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from models import Client

def index(request):
    return render(request, 'index.html')

def create_client(request):
    if request.method == 'GET':
        data = {}
        return render(request, 'new_client_form.html', data)

    if request.method == 'POST':
        data = request.POST
        
        client = Client()
        client.create_from_dict(data, 'user')
        client.save()
        
        return HttpResponse('Client saved')

def create_bid(request):
    if request.method == 'GET':
        data = {}
        return render(request, 'new_bid_form.html', data)

    if request.method == 'POST':
        return HttpResponse('BID saved')

def create_respondent(request):
    if request.method == 'GET':
        data = {}
        return render(request, 'new_respondent.html', data)

    if request.method == 'POST':
        return HttpResponseRedirect('../new_bid/')