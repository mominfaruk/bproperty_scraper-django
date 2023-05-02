import csv
import numpy as np
import pandas as pd
from .tasks import *
from .models import *
from datetime import datetime
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse


def home(request):
    return JsonResponse({"message": "Abrasives App is running!"})


def extract(request):
    platform = request.GET.get("platform", "")
    created = datetime.today().strftime("%Y-%m-%d")

    if Extraction.objects.filter(
            platform=platform
    ).exists() and not Extraction.objects.get(platform=platform).status:
        return JsonResponse({"message": "Task Already Running"})
    else:
        if platform:
            extraction_task.delay(platform, created)
            return JsonResponse({"message": "Task Started"})
        else:
            return JsonResponse({"message": "Invalid Parameters"})


# def get_csv_data(request):
#     platform = request.GET.get("platform", "")
#     created = request.GET.get("created", "")

#     if Extraction.objects.filter(platform=platform, created=created).exists():
#         if not Extraction.objects.get(platform=platform, created=created).status:
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = f'attachment; filename="{platform.title()}_Product_Data.csv"'

#             extraction = Extraction.objects.get(platform=platform, created=created)
#             if RawProductData.objects.filter(extraction=extraction).count() > MappedProductData.objects.filter(
#                     extraction=extraction).count():
#                 product_data = RawProductData.objects.filter(extraction=extraction)
#             else:
#                 product_data = MappedProductData.objects.filter(extraction=extraction)
#             product_data = [model_to_dict(data) for data in product_data]

#             for idx, _ in enumerate(product_data):
#                 product_data[idx]["brand"] = platform
#                 product_data[idx].pop("id")
#                 product_data[idx].pop("extraction")

#             writer = csv.writer(response, delimiter=',')
#             for idx, data in enumerate(product_data):
#                 if idx > 0:
#                     writer.writerow(data.values())
#                 else:
#                     writer.writerow(data.keys())

#             return response
#         else:
#             return JsonResponse({"message": "Scraper Already Running!"})
#     else:
#         return JsonResponse({"message": "No Extraction Found!"})
