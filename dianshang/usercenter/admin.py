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
