"""hanmei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from main import views as main_views

urlpatterns = [
    path('', main_views.index,name='index'),
    path('query/', main_views.search_json,name='search-json'),
    path('search/', main_views.search,name='search'),
    path('about/', main_views.about,name='about'),
    path('help/', main_views.help,name='help'),
    path('statistics/', main_views.stats,name='statistics'),
    path('download/file/<str:file_name>/', main_views.big_file_download,name='download-file'),
    path('download/', main_views.download,name='download'),
    path('detail/<str:site_name>/',main_views.site_json, name='site_detail'),
]
