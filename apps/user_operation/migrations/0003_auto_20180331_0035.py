# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-31 00:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20180325_2256'),
        ('user_operation', '0002_auto_20180310_1920'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set([('user', 'goods')]),
        ),
    ]
