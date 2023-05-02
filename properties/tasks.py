import os
from celery import shared_task
from .models import *
from datetime import datetime

@shared_task(bind=True)
def extraction_task(self):
    print("Extraction Started!")
    spider_path ="D:\Project\bdproperty\propertyproject\properties\scrapers"
    os.system(f"cd {spider_path} && scrapy crawl bikroy")
    print("Extraction Completed!!")