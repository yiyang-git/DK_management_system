from django.urls import path
from Manufacturing import views

urlpatterns = [
    path('add_receive/', views.add_receive),
    path('receive_table/', views.receive_table),
    path('add_unqual/', views.add_unqual),
    path('unqual_table/', views.unqual_table),
    path('edit_receive/', views.edit_receive),
    path('delete_receive', views.delete_receive),
    path('edit_unqual/', views.edit_unqual),
    path('delete_unqual/', views.delete_unqual),
    path('outer_table/', views.outer_table),
    path('add_outer/', views.add_outer),
    path('edit_outer/', views.edit_outer),
    path('delete_outer/', views.delete_outer)
]
