# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-06 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercenter', '0004_auto_20180506_0925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsort',
            options={'verbose_name': '商品分类', 'verbose_name_plural': '商品分类'},
        ),
    ]