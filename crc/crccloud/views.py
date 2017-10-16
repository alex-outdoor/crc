# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from models import Client

def create(request):
    if request.method == 'GET':
        data = {}
        return render(request, 'new_client_form.html', data)

    if request.method == 'POST':
        data = request.POST
        
        client = Client()
        client.create_from_dict(data, 'user')
        client.save()
        
        return HttpResponse('Client saved')
