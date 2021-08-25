from django.urls import path
from Knowledge import views

urlpatterns = [
    path('knowledge_add/', views.knowledge_add),
    path('knowledge_show/', views.knowledge_show),
    path('knowledge_manage/', views.knowledge_manage),
    path('edit_knowledge/', views.edit_knowledge),
    path('delete_knowledge/', views.delete_knowledge),
    path('delete_file/', views.delete_file)
]
