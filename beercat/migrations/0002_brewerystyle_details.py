# Generated by Django 3.0.5 on 2020-05-18 14:57

import beercat.models.mdfield
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beercat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewerystyle',
            name='details',
            field=beercat.models.mdfield.MDField(blank=True, null=True, verbose_name='Details'),
        ),
    ]