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

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number
from pylatex.utils import bold, NoEscape


@login_required
def export_bid(request, bid_id):
    
    if not bid_id:
        # test of PyLatex
        def generate_unique():
            geometry_options = {
                "head": "40pt",
                "margin": "0.5in",
                "bottom": "0.6in",
                "includeheadfoot": True
            }
            doc = Document(geometry_options=geometry_options)

            # Generating first page style
            first_page = PageStyle("firstpage")

            # Add document title
            with first_page.create(Head("R")) as right_header:
                with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c', align='r')) as title_wrapper:
                    title_wrapper.append(LargeText(bold("Bank Account Statement")))
                    title_wrapper.append(LineBreak())
                    title_wrapper.append(MediumText(bold("Date")))

            # Add footer
            with first_page.create(Foot("C")) as footer:
                message = "Important message please read"
                with footer.create(Tabularx(
                        "X X X X",
                        width_argument=NoEscape(r"\textwidth"))) as footer_table:

                    footer_table.add_row(
                        [MultiColumn(4, align='l', data=TextColor("blue", message))])
                    footer_table.add_hline(color="blue")
                    footer_table.add_empty_row()

                    branch_address = MiniPage(
                        width=NoEscape(r"0.25\textwidth"),
                        pos='t')
                    branch_address.append("960 - 22nd street east")
                    branch_address.append("\n")
                    branch_address.append("Saskatoon, SK")

                    document_details = MiniPage(width=NoEscape(r"0.25\textwidth"),
                                                pos='t', align='r')
                    document_details.append("1000")
                    document_details.append(LineBreak())
                    document_details.append(simple_page_number())

                    footer_table.add_row([branch_address, branch_address,
                                          branch_address, document_details])

            doc.preamble.append(first_page)
            # End first page style

            # Add customer information
            with doc.create(Tabu("X[l] X[r]")) as first_page_table:
                customer = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='h')
                customer.append("Verna Volcano")
                customer.append("\n")
                customer.append("For some Person")
                customer.append("\n")
                customer.append("Address1")
                customer.append("\n")
                customer.append("Address2")
                customer.append("\n")
                customer.append("Address3")

                # Add branch information
                branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
                                  align='r')
                branch.append("Branch no.")
                branch.append(LineBreak())
                branch.append(bold("1181..."))
                branch.append(LineBreak())
                branch.append(bold("TIB Cheque"))

                first_page_table.add_row([customer, branch])
                first_page_table.add_empty_row()

            doc.change_document_style("firstpage")
            doc.add_color(name="lightgray", model="gray", description="0.80")

            # Add statement table
            with doc.create(LongTabu("X[l] X[2l] X[r] X[r] X[r]",
                                     row_height=1.5)) as data_table:
                data_table.add_row(["date",
                                    "description",
                                    "debits($)",
                                    "credits($)",
                                    "balance($)"],
                                   mapper=bold,
                                   color="lightgray")
                data_table.add_empty_row()
                data_table.add_hline()
                row = ["2016-JUN-01", "Test", "$100", "$1000", "-$900"]
                for i in range(30):
                    if (i % 2) == 0:
                        data_table.add_row(row, color="lightgray")
                    else:
                        data_table.add_row(row)

            doc.append(NewPage())

            # Add cheque images
            # with doc.create(LongTabu("X[c] X[c]")) as cheque_table:
            #     cheque_file = os.path.join(os.path.dirname(__file__),
            #                                'chequeexample.png')
            #     cheque = StandAloneGraphic(cheque_file, image_options="width=200px")
            #     for i in range(0, 20):
            #         cheque_table.add_row([cheque, cheque])

            doc.generate_pdf("complex_report", clean_tex=False)

        generate_unique()
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
    