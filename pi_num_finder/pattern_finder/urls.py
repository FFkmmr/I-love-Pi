from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('search/', views.pi_search, name="pi_search"),
    path('pi-200mil-detail/<int:mil_id>/', views.pi_chunk_detail, name='pi_chunk_detail'),
    path('all', views.all_page, name='all_page'),
    path('clear-find-patterns/', views.clear_find_patterns, name='clear_find_patterns'),
    
]