"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

import osushop.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', osushop.views.welcometoindex),
    path('index', osushop.views.welcometoindex),
    path('register', osushop.views.register),
    path('login', osushop.views.login),
    path('issue_page', osushop.views.issue_form),
    path('logout', osushop.views.logout),
    path('workingon', osushop.views.workingon),
    path('good_detail', osushop.views.togood_detail_page),
    path('search', osushop.views.search),
    path('search2', osushop.views.search2),
    path('join_cart', osushop.views.join_cart),
    path('user_center', osushop.views.user_center),
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
