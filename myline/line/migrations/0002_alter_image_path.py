# Generated by Django 5.0.4 on 2024-05-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("line", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="path",
            field=models.ImageField(
                help_text="The image's path from the website", upload_to="media/"
            ),
        ),
    ]