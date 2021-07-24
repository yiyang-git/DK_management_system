from django.urls import path, re_path
from Helps import views
from tool11 import settings
from django.views.static import serve
import os

urlpatterns = [
    path('add_help/', views.add_help),
    path('help_table/', views.help_table),
    path('complete_help/', views.complete_help),
    path('add_suggest/', views.add_suggest),
    path('suggest_table/', views.suggest_table),
    path('complete_suggest/', views.complete_suggest),
    path('documentations/', views.documentations),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, "static")})
]
