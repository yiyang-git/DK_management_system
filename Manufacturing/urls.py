from django.urls import path
from Manufacturing import views

urlpatterns = [
    path('receive/', views.receive),
    path('receive_table/', views.receive_table),
    path('unqual/', views.unqual),
    path('unqual_table/', views.unqual_table),
]
