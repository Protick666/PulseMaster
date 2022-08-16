"""PulseMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

app_name = 'Outer_updates'
from .views import BindUpdateView, BindInitView, DemoView, BindUpdateViewV2
urlpatterns = [
    # path('update-bind/', BindUpdateView.as_view(), name='bind_update_api'),
    path('update-bind/v2/', BindUpdateViewV2.as_view(), name='bind_update_api_v2'),

    path('init-bind/', BindInitView.as_view(), name='bind_init_api'),
    path('demo/', DemoView.as_view(), name='bind_demo_api'),
]
