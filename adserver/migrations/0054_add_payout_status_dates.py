# Generated by Django 2.2.13 on 2021-06-15 01:46
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('adserver', '0053_add_regiontopic_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisherpayout',
            name='end_date',
            field=models.DateField(help_text='Last day of paid period', null=True, verbose_name='End Date'),
        ),
        migrations.AddField(
            model_name='publisherpayout',
            name='start_date',
            field=models.DateField(help_text='First day of paid period', null=True, verbose_name='Start Date'),
        ),
        migrations.AddField(
            model_name='publisherpayout',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('hold', 'On hold'), ('emailed', 'Email sent'), ('paid', 'Payment sent')], default='pending', help_text='Status of this payout', max_length=50),
        ),
    ]
