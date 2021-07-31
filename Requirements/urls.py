from django.urls import path
from Requirements import views

urlpatterns = [
    path('add_req/', views.add_req),
    path('req_list/', views.req_list),
    path('edit_req/', views.edit_req),
    path('delete_req/', views.delete_req),
    path('req_export/', views.req_export),
]
