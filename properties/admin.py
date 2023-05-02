from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Property)
@admin.register(Property)
class BpPropertyItem(admin.ModelAdmin):
    list_display= ['platform', 'commercial_type', 'property_url', 'property_description', 'property_overview',
     'price', 'location', 'num_bed_rooms', 'num_bath_rooms', 'area', 'building_type', 'purpose']
    list_filter = ('platform',)
admin.site.register(Platfroms)