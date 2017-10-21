# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Client, Bid, Respondent, Methodology, Deliverable

class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_name', 'contact_email', 'main_phone', 'province', 'country')
    
admin.site.register(Client, ClientAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ('topic', 'client')

admin.site.register(Bid, BidAdmin)

class RespondentAdmin(admin.ModelAdmin):
    list_display = ('city', 'type_respondent', 'nbr_respondent', 'bid')
    
admin.site.register(Respondent, RespondentAdmin)
