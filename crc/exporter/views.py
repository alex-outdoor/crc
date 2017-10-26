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

from pylatex import Document, Section, Figure, SubFigure, NoEscape
import os


@login_required
def export_bid(request, bid_id):
    
    if not bid_id:
        # test of PyLatex
        doc = Document(default_filepath='subfigures')
        image_filename = os.path.join(os.path.dirname(__file__), 'logo.jpg')

        with doc.create(Section('Showing subfigures')):
            with doc.create(Figure(position='h!')) as kittens:
                with doc.create(SubFigure(
                        position='b',
                        width=NoEscape(r'0.45\linewidth'))) as left_kitten:

                    left_kitten.add_image(image_filename,
                                          width=NoEscape(r'\linewidth'))
                    left_kitten.add_caption('Kitten on the left')
                with doc.create(SubFigure(
                        position='b',
                        width=NoEscape(r'0.45\linewidth'))) as right_kitten:

                    right_kitten.add_image(image_filename,
                                           width=NoEscape(r'\linewidth'))
                    right_kitten.add_caption('Kitten on the right')
                kittens.add_caption("Two kittens")

        doc.generate_pdf("/var/crc_project/crc/templates/latex/crc", clean_tex=False)

        return HttpResponse(200)
    
    # Database informations
    base_url = request.scheme + '://' + request.META['HTTP_HOST']
    url =  base_url + '/api/bid/' + bid_id
    
    # LaTeX images seems to need absolute file path
    absolute_path = os.path.abspath(os.path.dirname(__file__))
    crc_dir = '/'.join(absolute_path.split('/')[0:-2])

    response = requests.get(url)
    if(response.ok):
        
        # Download image from /static/
        logo_url = base_url + '/static/img/logo.jpg'
        # logo_response = requests.get(url)
        # if logo_response.ok:
        #     logo_tempdir = tempfile.mkdtemp()
        #     with open(os.path.join(logo_tempdir, 'logo.jpg'), 'wb') as f:
        #         f.write(logo_response.content)

        #r = requests.get(logo_url, stream=True)
        #r.raise_for_status()
        #r.raw.decode_content = True  # Required to decompress gzip/deflate compressed responses.
        #with open('/var/logo.jpg', 'wb') as f:
        #    r.raw.decode_content = True
        #    shutil.copyfileobj(r.raw, f)
        #r.close()  # Safety when stream=True ensure the connection is released.
                
        data = json.loads(response.content)
        
        context = {  
            'topic': data['topic'],
            'company': data['client']['company_name'],
            'contact_name': data['contact_name'] if data['contact_name'] else data['client']['contact_name'],
            'contact_email': data['contact_email'] if data['contact_name'] else data['client']['contact_email'],
            'respondents' : data['respondents'],
            'logo' : '/var/logo.jpg',
            'creationDate': 'Date of BID or of today ?',
        }
    
        template = get_template('latex/latex_template.tex')
        rendered_tpl = template.render(context).encode('utf-8')
        
        #subprocess.call(['pdflatex', rendered_tpl])
        
        #tempdir = tempfile.mkdtemp()
        
        #for i in range(2):
        process = Popen(['pdflatex', '-output-directory', crc_dir + '/crc/templates/latex', '--shell-escape'], stdin=PIPE)
        process.communicate(rendered_tpl)
        
        #with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
        #    pdf = f.read()
        
        #r = HttpResponse(content_type='application/pdf')
        #r['Content-Disposition'] = 'attachment; filename=texput.pdf' #Downloadable pdf from the browser
        #r.write(pdf)
        #shutil.rmtree(tempdir)
        return HttpResponse(200)
    
    else:
        return HttpResponse(404)
    