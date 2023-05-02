from django.db import models
from django.contrib.auth.models import User


class  Platfroms(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True)
    creted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} ({self.creted_at})'

class Property(models.Model):
    platform = models.ForeignKey(Platfroms, on_delete=models.CASCADE)
    commercial_type = models.CharField(max_length=50, blank=True, null=True)
    property_url = models.URLField(max_length=200, blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    property_overview = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    num_bed_rooms = models.CharField(max_length=100,blank=True, null=True)
    num_bath_rooms = models.CharField(max_length=100,blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    building_type = models.CharField(max_length=50, blank=True, null=True)
    purpose = models.CharField(max_length=50, blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.property_description} ({self.price})'


