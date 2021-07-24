from django.urls import path
from Experiment import views

urlpatterns = [
    path('add_test/', views.add_test),
    path('test_table/', views.test_table),
    path('edit_test/', views.edit_test),
    path('delete_test/', views.delete_test),
]
