# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User

# Base class with recurrent attributes
class Base(models.Model):
    class Meta:
        app_label = 'crccloud'
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True,
        help_text="Created date")
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True,
        help_text="Updated date")
    # created_by = models.ForeignKey(User, blank=True, null=True,
    #     help_text="Creator")
        
# Definition of a client
class Client(Base):
    company_name = models.CharField(max_length=100, blank=True, null=True,
        help_text="Name of the company")
    contact_name = models.CharField(max_length=100, blank=True, null=True,
        help_text="Name of the contact")
    contact_email = models.EmailField('email address', max_length=254, blank=True, null=True, 
        help_text="Email of the contact")
    address = models.CharField(max_length=200, blank=True, null=True,
        help_text="Address")   
    postal_code = models.CharField(max_length=20, blank=True, null=True,
        help_text="Postal Code")
    city = models.CharField(max_length=50, blank=True, null=True,
        help_text="City")
    province = models.CharField(max_length=50, blank=True, null=True,
        help_text="Province")
    country = models.CharField(max_length=30, blank=True, null=True,
        help_text="Country")
    main_phone = models.CharField(max_length=30, blank=True, null=True,
        help_text="Main phone number")
    direct_number = models.CharField(max_length=30, blank=True, null=True,
        help_text="Direct number")
    fax = models.CharField(max_length=30, blank=True, null=True,
        help_text="Fax number")
    notes = models.CharField(max_length=500, blank=True, null=True,
        help_text="Notes")


    def __str__(self):
        return self.company_name + ' - ' + self.contact_name

    def as_dict(self):
        return {
            'company_name': self.company_name,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'created by': self.created_by.name, 
            'created': self.created_date
        }

    def create_from_dict(self, data, user):
        #self.created_by = user
        self.company_name = data.get('company_name', '')
        self.contact_name = data.get('contact_name', '')
        self.contact_email = data.get('contact_email', '')
        self.address = data.get('address', '')
        self.postal_code = data.get('postal_code', '')
        self.city = data.get('city', '')
        self.province = data.get('province', '')
        self.country = data.get('country', '')
        self.main_phone = data.get('main_phone', '')
        self.direct_number = data.get('direct_number', '')
        self.fax = data.get('fax', '')
        self.notes = data.get('notes', '')
        return self