# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template


from subprocess import Popen, PIPE
import tempfile
import os
import shutil 
import requests
import json

from crccloud.models import Client, Bid, Respondent, Methodology, Deliverable

@login_required
def export_bid(request, bid_id):
    # Database informations
    url = request.scheme + '://' + request.META['HTTP_HOST'] + '/api/bid/' + bid_id
    response = requests.get(url)
    if(response.ok):
        data = json.loads(response.content)
        
        context = {  
            'topic': data['topic'],
            'company': data['client']['company_name'],
            'nbr_groups' : len(data['respondents']),
        }
    
        template = get_template('latex_template.tex')
        rendered_tpl = template.render(context).encode('utf-8')
    
        tempdir = tempfile.mkdtemp()
        
        for i in range(2):
            process = Popen(['pdftex', '-output-directory', tempdir], stdin=PIPE, stdout=PIPE)
            process.communicate(rendered_tpl)
        
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
        
        shutil.rmtree(tempdir)
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=texput.pdf' #Downloadable pdf from the browser
        r.write(pdf)
        return r
    