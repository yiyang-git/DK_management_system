from django.urls import path
from Maintenance import views

urlpatterns = [
    path('add_runRecord/', views.add_runRecord),
    path('runRecord_table/', views.runRecord_table),
    path('add_fault/', views.add_fault),
    path('fault_table/', views.fault_table),
    path('edit_runRecord/', views.edit_runRecord),
    path('delete_runRecord', views.delete_runRecord),
    path('edit_fault/', views.edit_fault),
    path('delete_fault/', views.delete_fault)
]
