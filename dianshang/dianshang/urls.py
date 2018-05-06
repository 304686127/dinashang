"""dianshang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import django
from dianshang import settings
from django.contrib import admin
from django.views.static import serve
# 这里我修改了一下，不然我的显示'django.views.static' is not a package


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^', include('usercenter.urls')),
]
