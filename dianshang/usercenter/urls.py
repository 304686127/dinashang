# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^indexapi/$', views.view_index),
    url(r'^goodlist/$', views.view_good_list),
    url(r'^gooddetial/([0-9])/$', views.view_good_detial),
    url(r'^cartlist/$', views.view_cart),
]
