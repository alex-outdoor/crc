# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template
from django.utils.formats import date_format

from subprocess import Popen, PIPE
#import subprocess
import tempfile
import os
import shutil 
import requests
import json
import PIL
from datetime import datetime

from django.conf import settings
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response

@login_required
def export_bid(request, bid_id):

    # Database informations
    base_url = request.scheme + '://' + request.META['HTTP_HOST']
    url =  base_url + '/api/bid/' + bid_id

    response = requests.get(url)
    if(response.ok):    
        data = json.loads(response.content)
        
        sub_total_recruitment = 0
        sub_total_incentive = 0
        for resp in data['respondents']:
            sub_total_recruitment += resp['recruitment_total']
            sub_total_incentive += resp['incentive_total'] # Part from respondent
        
        incentive_handling_total = data['incentive_handling_unit_cost'] * data['incentive_handling_qte']
        sub_total_incentive += incentive_handling_total
           
        facility_rental_total = data['facility_rental_unit_cost'] * data['facility_rental_qte']
        refreshments_respondent_total = data['refreshments_respondent_unit_cost'] * data['refreshments_respondent_qte']
        
        sub_total_facility = data['catering_client'] + refreshments_respondent_total + facility_rental_total
        
        moderation_total = data['moderation_unit_cost'] * data['moderation_qte']
        sub_total_moderation = moderation_total + data['moderator_briefing'] + data['moderator_travel']
        
        sub_total_translation = data['simultaneous_translation'] + data['translation_cost']
        
        context = {  
            'today': datetime.now(),
            'topic': data['topic'],
            'company': data['client']['company_name'],
            'contact_name': data['contact_name'] if data['contact_name'] else data['client']['contact_name'],
            'contact_email': data['contact_email'] if data['contact_name'] else data['client']['contact_email'],
            'respondents' : data['respondents'],
            'bid_notes': data['notes'],
            'recruitment': data['recruitment_duration'],
            'data': data,
            'sub_total_recruitment': sub_total_recruitment,
            'sub_total_incentive': sub_total_incentive,
            'incentive_handling_total': incentive_handling_total,
            'facility_rental_total' : facility_rental_total,
            'refreshments_respondent_total': refreshments_respondent_total,
            'sub_total_facility': sub_total_facility,
            'moderation_total': moderation_total,
            'sub_total_moderation': sub_total_moderation,
            'sub_total_translation': sub_total_translation,
        }
    
        template = 'pdf_bid.html'

        pdf = render_to_pdf_response(request, template, context, using=None, 
            download_filename=None, content_type='application/pdf', 
            response_class=HttpResponse)
            
        return pdf
        #return render(request, template, context)