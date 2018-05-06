# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.UserInfo)
admin.site.register(models.Cart)
admin.site.register(models.Orders)
admin.site.register(models.OrderDetail)
admin.site.register(models.AddrInfo)
admin.site.register(models.GoodSort)
admin.site.register(models.Goods)
admin.site.register(models.Copa)
admin.site.register(models.index_img)
