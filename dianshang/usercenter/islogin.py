# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
import functools


# 一个装饰器，判断是否登录，如果没有就转到登录界面
def islogin(func):
    @functools.wraps(func)
    def login_func(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            return

    return login_func
