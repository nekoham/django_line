# Generated by Django 5.0.4 on 2024-05-13 04:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Website",
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
                    "url",
                    models.CharField(
                        help_text="The website's url for images", max_length=200
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Date of creation"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
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
                    "path",
                    models.CharField(
                        help_text="The image's path from the website", max_length=200
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Date of creation"
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image_source",
                        to="line.website",
                    ),
                ),
            ],
        ),
    ]
