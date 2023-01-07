# Generated by Django 3.2.16 on 2022-12-31 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=40)),
                ('vehicle_name', models.CharField(max_length=255)),
                ('registration_no', models.CharField(max_length=20)),
                ('daily_min_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('daily_max_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_min_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_max_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.CharField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]