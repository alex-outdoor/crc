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
def create_client(request, client_id):
    if request.method == 'GET':
        if client_id:
            client = Client.objects.get(id=client_id)
            data = client.as_dict()
        else:
            data = {}
            
        data['client_id'] = client_id
        return render(request, 'new_client_form.html', data)

    if request.method == 'POST':
        data = request.POST
        if client_id:
            client = Client.objects.get(id=client_id)
        else:
            # Creating a new client
            client = Client()
        client.create_from_dict(data, request.user)
        client.save()

        return HttpResponseRedirect('/crc/list_clients')
    
@login_required
def create_bid(request, bid_id):
    if request.method == 'GET':
        data = {}
        if bid_id:
            # When editing a bid
            bid = Bid.objects.get(id=bid_id)
            data = bid.as_dict()
            
        data['bid_id'] = bid_id
        return render(request, 'new_bid_form.html', data)
    
    if request.method == 'POST':
        data = request.POST

        if not bid_id:
            # Create a new database Bid
            bid = Bid()
        else:
            # When editing
            bid = Bid.objects.get(id=bid_id)
            
            # Delete Respondents group
            #edit_respondents = Respondent.objects.filter(bid__id=bid_id)
            #resp_ids = [x.id for x in edit_respondents]
            Respondent.objects.filter(bid__id=bid_id).delete()
            # Delete Deliverables
            #edit_deliverables = Deliverable.objects.filter(bid__id=bid_id)
            Deliverable.objects.filter(bid__id=bid_id).delete()
            #deliv_names = [x.name for x in edit_deliverables]
            #deliv_ids = [x.id for x in edit_deliverables]
        print data
        bid.create_from_dict(data, request.user)
        bid.save()
        
        # if bid_id:
        #     nbr_group = len(resp_ids)
        # else:
            # Number of respondent group
        nbr_group = int(data.get("saved_groups", '0'))
            
        i = 0 
        while (i<nbr_group):
            #if not bid_id:
                # Create a respondent group
            respondent = Respondent()
            #else:
                #respondent = Respondent.objects.get(id=nbr_group[i])
                
            respondent.create_from_dict(data, request.user, bid, str(i))
            respondent.save()
            
            #if not bid_id:
                # Now it's one methodology per client but that might change
            methodology = Methodology()
            #else:
                #methodology = Methodology.objects.get(respondent__id=nbr_group[i])
                
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
            'other_deliverable': data.get('other_deliverable', '')
        }
        
        for key in deliverables.keys():
            qty = data.get(key + '_qty','')
            
            name = key
            if key == 'other_deliverable':
                name = deliverables[key]
                
            # Case (1) : Creating a BID
            if qty != '':
                x = int(qty)
                deliverable = Deliverable()
                
                deliverable.create_from_dict(data, request.user, bid, key, x, name)
                deliverable.save()
                    
            # # Case (2) : Editing a BID
            # if bid_id:
            #     if key in deliv_names:
            #         # Editing existing deliverables
            #         index = deliv_names.index(key)
            #         deliv_id = deliv_ids[index]
            #         deliverable = Deliverable.objects.get(id=deliv_id)
            #         print bid, key, x, name
            #         deliverable.create_from_dict(data, request.user, bid, key, x, name)
            #         #deliverable.save()
            #     else:
            #         # Could be new one or other_deliverable
            #         deliverable = Deliverable()
            #         deliverable.create_from_dict(data, request.user, bid, key, x, name)
            #         #deliverable.save()
            #         #TO DO: Deal with other deliverables 
        return HttpResponseRedirect('/crc/list_bids')

@login_required
def list_clients(request):
    if request.method == 'GET':
        return render(request, 'list_client.html', {})
    
@login_required
def list_bids(request):
    if request.method == 'GET':
        return render(request, 'list_bids.html', {})
        
        
        
        
        
        
        
        
        
        