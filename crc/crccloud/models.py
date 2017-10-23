# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Base class with recurrent attributes
class Base(models.Model):
    class Meta:
        app_label = 'crccloud'
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True,
        help_text="Created date")
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True,
        help_text="Updated date")
    created_by = models.ForeignKey(User, blank=True, null=True,
         help_text="Creator")
        
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
            'address': self.address,
            'postal_code': self.postal_code,
            'city': self.city,
            'province': self.province,
            'country': self.country,
            'main_phone': self.main_phone,
            'direct_number': self.direct_number,
            'fax': self.fax,
            'notes': self.notes,
        }

    def create_from_dict(self, data, user):
        self.created_by = user
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

# Utils function
def get_attribute_value(data, attr):
    value = data.get(attr, '')
    if value == '': #default value in html
        value = '0'
    return value

# Definition of a BID
class Bid(Base):
    # Basic info
    topic = models.CharField(max_length=200, blank=True, null=True,
        help_text="Potential name of the project")
    client = models.ForeignKey("Client", related_name="bid_client", blank=True, null=True,
        help_text="Client for this BID")
    recruitment_duration = models.CharField(max_length=50, blank=True, null=True,
        help_text="Recruitment duration")
    currency = models.CharField(max_length=5, blank=True, null=True,
        help_text="Currency for this BID")
    project_mngt_cost = models.FloatField(blank=True, null=True,
        help_text="Project management cost")
    # Incentive handling
    incentive_handling_unit_cost = models.FloatField(blank=True, null=True,
        help_text="Incentive handling unit cost")
    incentive_handling_qte = models.FloatField(blank=True, null=True,
        help_text="Incentive handling quantity")
    # Catering / Refreshments
    catering_client = models.FloatField(blank=True, null=True,
        help_text="Catering for the client")
    refreshments_respondent_unit_cost = models.FloatField(blank=True, null=True,
        help_text="Refreshment unit cost")
    refreshments_respondent_qte = models.FloatField(blank=True, null=True,
        help_text="Refreshment quantity")
    # Moderation
    moderation_unit_cost = models.FloatField(blank=True, null=True,
        help_text="Moderation unit cost")
    moderation_qte = models.FloatField(blank=True, null=True,
        help_text="Moderation quantity")
    moderator_briefing = models.FloatField(blank=True, null=True,
        help_text="Moderator briefing")
    moderator_travel = models.FloatField(blank=True, null=True,
        help_text="Moderator travel")
    # Translation
    simultaneous_translation = models.FloatField(blank=True, null=True,
        help_text="Simultaneous translator")
    translation_words = models.FloatField(blank=True, null=True,
        help_text="Estimation of words to translate")
    translation_cost = models.FloatField(blank=True, null=True,
        help_text="Translation cost")
    # Facility
    facility_duration = models.CharField(max_length=50, blank=True, null=True,
        help_text="Facility rental duration")
    facility_rental_unit_cost = models.FloatField(blank=True, null=True,
        help_text="Facility rental unit cost")
    facility_rental_qte = models.FloatField(blank=True, null=True,
        help_text="Facility rental quantity")
    # Notes
    notes = models.CharField(max_length=300, blank=True, null=True,
        help_text="Notes")

    def __str__(self):
        return self.topic

    def create_from_dict(self, data, user):
        self.created_by = user
        self.topic = data.get('topic', '')
        client_id = float(data.get('client_id', '-1'))
        if client_id > 0:
            client = Client.objects.get(pk=client_id)
            self.client = client
        self.recruitment_duration = data.get('recruitment_duration', '')
        self.currency = data.get('currency', '')
        self.project_mngt_cost = float(data.get('project_management', '0'))
        self.incentive_handling_qte = float(get_attribute_value(data,'incentive_handling_units'))
        self.incentive_handling_unit_cost = float(get_attribute_value(data,'incentive_handling_unit_cost'))
        self.catering_client = float(get_attribute_value(data,'catering_client'))
        self.refreshments_respondent_qte = float(get_attribute_value(data,'refreshment_units'))
        self.refreshments_respondent_unit_cost = float(get_attribute_value(data,'refreshment_unit_cost'))
        self.moderation_qte = float(get_attribute_value(data,'moderation_units'))
        self.moderation_unit_cost = float(get_attribute_value(data,'moderation_unit_cost'))
        self.moderator_travel = float(get_attribute_value(data,'moderator_travel'))
        self.moderator_briefing = float(get_attribute_value(data,'moderator_briefing'))
        self.simultaneous_translation = float(get_attribute_value(data,'simultaneous_translator'))
        self.translation_cost = float(get_attribute_value(data,'translation_total2'))
        self.translation_words = float(get_attribute_value(data,'translation_words'))
        self.facility_rental_qte = float(get_attribute_value(data,'facility_units'))
        self.facility_duration = data.get('facility_duration', '')
        self.facility_rental_unit_cost = float(get_attribute_value(data,'facility_unit_cost'))
        self.notes = data.get('notes_bid', '')
        return self
    
    def as_dict(self):
        return {
            'topic': self.topic,
            'client': self.client,
            'currency': self.currency,
            'recruitment_duration': self.recruitment_duration,
            'project_management': self.project_mngt_cost,
            'incentive_handling_units': self.incentive_handling_qte,
            'incentive_handling_unit_cost': self.incentive_handling_unit_cost,
            'catering_client': self.catering_client,
            'moderation_units': self.moderation_qte,
            'moderation_unit_cost': self.moderation_unit_cost,
            'moderator_travel': self.moderator_travel,
            'moderator_briefing': self.moderator_briefing,
            'simultaneous_translator': self.simultaneous_translation,
            'translation_total': self.translation_cost,
            'translation_words': self.translation_words,
            'facility_units': self.facility_rental_qte,
            'facility_duration': self.facility_duration,
            'facility_unit_cost': self.facility_rental_unit_cost,
            'refreshments_respondent_unit_cost': self.refreshments_respondent_unit_cost,
            'refreshments_respondent_units': self.refreshments_respondent_qte,
            'notes': self.notes
        }

# Definition of a respondent group
class Respondent(Base):
    city = models.CharField(max_length=200, blank=True, null=True,
        help_text="Location of the test")
    type_respondent = models.CharField(max_length=200, blank=True, null=True,
        help_text="Type of respondent")
    nbr_respondent = models.FloatField(blank=True, null=True,
        help_text="Number of respondent(s)")
    over_recruitment = models.FloatField(blank=True, null=True,
        help_text="Over recruitment")
    bid = models.ForeignKey("Bid", related_name="respondents",
        help_text="Respondent group attached to this BID")
    language = models.CharField(max_length=20,blank=True, null=True,
        help_text="Language of test")
    incentive = models.FloatField(blank=True, null=True,
        help_text="Incentive per respondent")
    recruitment_cost = models.FloatField(blank=True, null=True,
        help_text="Recruitment cost per respondent")
    notes = models.TextField(blank=True, null=True,
        help_text="Notes")

    def create_from_dict(self, data, user, bid, index):
        self.created_by = user
        self.city = data.get('city_'+index, '')
        self.bid = bid
        self.type_respondent = data.get('type_respondent_'+index, '')
        self.language = data.get('language_'+index, '')
        self.nbr_respondent = float(data.get('nbr_respondent_'+index))
        self.over_recruitment = float(get_attribute_value(data,'nbr_over_recruitment_'+index))
        self.incentive = float(get_attribute_value(data,'incentive_'+index))
        self.recruitment_cost = float(get_attribute_value(data,'recruitment_cost_'+index))
        self.notes = data.get('notes_respondent_'+index, '')
        return self
        
    def __str__(self):
        return str(self.nbr_respondent) + ' - ' + self.type_respondent + ' - ' + self.city
    
# Definition of a methodology (Mostly if multiple methodolies can be attached to 1 respondent group)
class Methodology(Base):
    name = models.CharField(max_length=200, blank=True, null=True,
        help_text="Name of the test")
    duration = models.CharField(max_length=200, blank=True, null=True,
        help_text="Duration of the test")
    start_date = models.DateTimeField(blank=True, null=True,
        help_text="Start date")
    end_date = models.DateTimeField(blank=True, null=True,
        help_text="Start date")
    respondent = models.ForeignKey("Respondent", related_name="methodologies",
        help_text="Methodology linked to this respondent group")
        
    def create_from_dict(self, data, user, respondent, index):
        self.created_by = user
        self.duration = data.get('duration_'+index, '')
        self.respondent = respondent
        self.notes = data.get('notes_deliverable', '')
        test_name = data.get('radio_'+index, '')
        if test_name != 'other_test':
            self.name = data.get('radio_'+index, '')
        else:
            self.name = data.get('other_test_name_'+index, '')

        return self

# Definition of the deliverables
class Deliverable(Base):
    name = models.CharField(max_length=200, blank=True, null=True,
        help_text="Name of the deliverables")
    unit_cost = models.FloatField(blank=True, null=True,
        help_text="Unit cost")
    quantity = models.FloatField(blank=True, null=True,
        help_text="Quantity")
    duration = models.FloatField(blank=True, null=True,
        help_text="Duration")
    bid = models.ForeignKey("Bid", related_name="deliverable_bid",
        help_text="Deliverable attached to this BID")
    notes = models.TextField(blank=True, null=True,
        help_text="Notes")
    bid = models.ForeignKey("Bid", related_name="deliverables",
        help_text="Deliverables linked to this BID")

    def create_from_dict(self, data, user, bid, key, x, name):
        self.created_by = user
        self.unit_cost = float(get_attribute_value(data, key+'_cost'))
        self.quantity = x
        self.name = name
        self.bid = bid
        self.duration = float(get_attribute_value(data, key+'_duration'))
        self.notes = data.get('notes_deliverable', '')
        
        return self        
        