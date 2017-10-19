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
        return render(request, 'new_bid_form.html')

    if request.method == 'POST':
        data = request.POST
        #print data.get('topic', None)
        print data.get('nbr_respondent_0', None)
        #print data.get('english_to_english_cost', None)
        return HttpResponse('BID saved')

def create_respondent(request):
    if request.method == 'GET':
        return render(request, 'new_respondent.html')
