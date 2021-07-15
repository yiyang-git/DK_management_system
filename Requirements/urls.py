from django.urls import path
from Requirements import views

urlpatterns = [
    path('add_req/', views.add_req),
    path('req_list/', views.req_list),
]
