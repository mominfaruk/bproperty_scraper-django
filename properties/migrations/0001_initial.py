# Generated by Django 4.2 on 2023-04-16 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "commercial_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("property_url", models.URLField(blank=True, null=True)),
                ("property_description", models.TextField(blank=True, null=True)),
                ("property_overview", models.TextField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "num_bed_rooms",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "num_bath_rooms",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("area", models.TextField(blank=True, null=True)),
                (
                    "building_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("purpose", models.CharField(blank=True, max_length=50, null=True)),
                ("amenities", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
