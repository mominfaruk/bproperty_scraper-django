# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item, Field
#import django models
from properties.models import *
# from asgiref.sync import sync_to_async
# import traceback

class BpPropertyItem(Item):
    commercial_type = Field()
    property_url = Field()
    property_description = Field()
    property_overview = Field()
    price = Field()
    location = Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    area = Field()
    building_type = Field()
    purpose = Field()
    amenities = Field()

class BikroyItem(scrapy.Item):
    location = Field()
    area = Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    completion_status = Field()
    facing = Field()
    commercial_type = Field()
    building_type = Field()
    price = Field()
    property_url = Field()
    property_description = Field()