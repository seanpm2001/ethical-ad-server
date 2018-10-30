# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-19 22:39
from __future__ import unicode_literals

import datetime

import django.core.validators
import django.db.models.deletion
import django.utils.crypto
import django_countries.fields
import jsonfield.fields
from django.db import migrations
from django.db import models

import adserver.models
import adserver.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdImpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('offers', models.IntegerField(default=0, help_text='The number of times an ad was proposed by the ad server. The client may not load the ad (a view) for a variety of reasons ', verbose_name='Offers')),
                ('views', models.IntegerField(default=0, help_text='Number of times the ad was legitimately viewed', verbose_name='Views')),
                ('clicks', models.IntegerField(default=0, help_text='Number of times the ad was legitimately clicked', verbose_name='Clicks')),
            ],
            options={
                'verbose_name_plural': 'Ad impressions',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.CharField(max_length=200, verbose_name='Slug')),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('link', models.URLField(blank=True, max_length=255, null=True, verbose_name='Link URL')),
                ('image', models.URLField(blank=True, help_text='240x180', max_length=255, null=True, verbose_name='Image URL')),
                ('live', models.BooleanField(default=False, verbose_name='Live')),
            ],
            options={
                'ordering': ('slug', '-live'),
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, verbose_name='Campaign Slug')),
                ('secret', models.SlugField(default=django.utils.crypto.get_random_string, help_text='A secret required to view advertisement reports', verbose_name='Report Secret')),
                ('campaign_type', models.CharField(choices=[('paid', 'Paid'), ('community', 'Community'), ('house', 'House')], default='paid', max_length=20, verbose_name='Campaign Type')),
                ('max_sale_value', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='If set, ads will not be displayed if (cpc * total_clicks) + (cpm * total_views / 1000) for all ads exceeds this', max_digits=8, null=True, verbose_name='Max Sale Value')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('ip', models.GenericIPAddressField(verbose_name='Ip Address')),
                ('user_agent', models.CharField(blank=True, max_length=1000, null=True, verbose_name='User Agent')),
                ('client_id', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Client ID')),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('url', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Page URL')),
                ('browser_family', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Browser Family')),
                ('os_family', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Operating System Family')),
                ('is_bot', models.BooleanField(default=False)),
                ('is_mobile', models.BooleanField(default=False)),
                ('advertisement', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.PROTECT, related_name='clicks', to='adserver.Advertisement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, verbose_name='Flight Slug')),
                ('start_date', models.DateField(default=datetime.date.today, help_text='This ad will not be shown before this date', verbose_name='Start Date')),
                ('end_date', models.DateField(default=adserver.models.default_flight_end_date, help_text='The target end date for the ad (it may go after this date)', verbose_name='End Date')),
                ('live', models.BooleanField(default=False, verbose_name='Live')),
                ('priority_multiplier', models.IntegerField(default=1, help_text="Multiplies chance of showing this flight's ads [1,100]", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Priority Multiplier')),
                ('cpc', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Cost Per Click')),
                ('sold_clicks', models.IntegerField(default=0, verbose_name='Sold Clicks')),
                ('cpm', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Cost Per 1k Impressions')),
                ('sold_impressions', models.IntegerField(default=0, verbose_name='Sold Impressions')),
                ('targeting_parameters', jsonfield.fields.JSONField(blank=True, null=True, validators=[adserver.validators.TargetingParametersValidator()], verbose_name='Targeting parameters')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flights', to='adserver.Campaign')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('ip', models.GenericIPAddressField(verbose_name='Ip Address')),
                ('user_agent', models.CharField(blank=True, max_length=1000, null=True, verbose_name='User Agent')),
                ('client_id', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Client ID')),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('url', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Page URL')),
                ('browser_family', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Browser Family')),
                ('os_family', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='Operating System Family')),
                ('is_bot', models.BooleanField(default=False)),
                ('is_mobile', models.BooleanField(default=False)),
                ('advertisement', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.PROTECT, related_name='views', to='adserver.Advertisement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='advertisement',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='advertisements', to='adserver.Flight'),
        ),
        migrations.AddField(
            model_name='adimpression',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='impressions', to='adserver.Advertisement'),
        ),
        migrations.AlterUniqueTogether(
            name='adimpression',
            unique_together=set([('advertisement', 'date')]),
        ),
    ]
