# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-10 14:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_goodscategorybrand_cagetor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='cagetor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品类目'),
        ),
    ]