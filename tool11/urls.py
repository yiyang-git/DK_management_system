"""
tool11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', view.show_homepage),
    path('', view.show_homepage),
    path('Requirements/', include('Requirements.urls')),  # include是为了将子项目的url完成拼接
    path('Manufacturing/', include('Manufacturing.urls')),
    path('Maintenance/', include('Maintenance.urls')),
    path('Experiment/', include('Experiment.urls')),
    path('Helps/', include('Helps.urls')),
    path('Statistics/', include('Statistics.urls')),
    path('Search/', include('Search.urls'))
]
