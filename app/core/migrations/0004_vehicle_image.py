# Generated by Django 3.2.16 on 2023-01-07 09:14

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_agreement_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.vehicle_image_file_path),
        ),
    ]
