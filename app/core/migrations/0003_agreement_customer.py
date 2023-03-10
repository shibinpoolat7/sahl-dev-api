# Generated by Django 3.2.16 on 2023-01-05 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_type', models.CharField(max_length=40)),
                ('customer_name', models.CharField(max_length=255)),
                ('cr_id_no', models.CharField(max_length=40)),
                ('customer_email', models.EmailField(max_length=100)),
                ('customer_mobile', models.CharField(max_length=100)),
                ('customer_phone', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('customer_address', models.TextField(blank=True, default=None, null=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_type', models.CharField(max_length=50)),
                ('agreement_no', models.CharField(max_length=255)),
                ('deposit_type', models.CharField(max_length=40)),
                ('external_customer_name', models.EmailField(blank=True, default=None, max_length=255, null=True)),
                ('checkin_date', models.DateField()),
                ('checkout_date', models.DateField(blank=True, default=None, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agreement_customer', to='core.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agreement_vehicle', to='core.vehicle')),
            ],
        ),
    ]
