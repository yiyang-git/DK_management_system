from django.urls import path
from Statistics import views

urlpatterns = [
    path('statistics_req/', views.statistics_req),
    path('statistics_man/', views.statistics_man),
    path('statistics_mtn/', views.statistics_mtn),
    path('statistics_exp/', views.statistics_exp),
    path('statistics_custom/', views.statistics_custom)
]
