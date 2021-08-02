from django.urls import path
from Search import views

urlpatterns = [
    path('search/', views.search)
]
