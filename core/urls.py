# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import admin
from django.urls import path, include # add this

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin_page_16/', admin.site.urls),                # Django admin route
    path('', include('apps.authentication.urls')),  # Auth routes - login / register
    path('', include('apps.home.urls')),            # UI Kits Html files
    path('spm/', include('apps.spamer.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
