# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-06 17:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20180310_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='trade.OrderInfo', verbose_name='订单信息'),
        ),
    ]
