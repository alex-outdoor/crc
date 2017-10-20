# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from models import Client, Bid, Respondent, Methodology, Deliverable

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def create_client(request):
    if request.method == 'GET':
        data = {}
        return render(request, 'new_client_form.html', data)

    if request.method == 'POST':
        data = request.POST
        
        client = Client()
        client.create_from_dict(data, request.user)
        client.save()

        return HttpResponseRedirect('/crc/list_clients')

@login_required
def create_bid(request):
    if request.method == 'GET':
        return render(request, 'new_bid_form.html')

    if request.method == 'POST':
        data = request.POST
        
        # Create/Save a new database Bid 
        bid = Bid()
        bid.create_from_dict(data, request.user)
        bid.save()
        
        # Number of respondent group
        nbr_group = int(data.get("saved_groups", '0'))
        i = 0 
        while (i<nbr_group):
            # Create a respondent group
            respondent = Respondent()
            respondent.create_from_dict(data, request.user, bid, str(i))
            respondent.save()
            
            # Now it's one methodology per client but that might change
            methodology = Methodology()
            methodology.create_from_dict(data, request.user, respondent, str(i))
            methodology.save()
            
            i += 1
            
        # Create / Save Deliverables if quantity is not null
        deliverables = {
            'english_to_english':'Transcripts from English to English',
            'french_to_english':'Transcripts from French to English',
            'content_analysis':'Content Analysis',
            'topline_report':'Topline report',
            'full_report':'Full Report',
            'summary_report':'Summary Report',
            'discussion_guide_design':'Discussion Guide Design',
            'screener_design':'Screener Design',
            'other_test': data.get('other_test_name', '')
        }
        
        for key in deliverables.keys():
            qty = data.get(key + '_qty','')
            if qty != '':
                x = int(qty)
                deliverable = Deliverable()
                deliverable.create_from_dict(data, request.user, bid, key, x, deliverables[key])
                deliverable.save()
            
        return HttpResponse('BID saved')

@login_required
def list_clients(request):
    if request.method == 'GET':
        return render(request, 'list_client.html', {})