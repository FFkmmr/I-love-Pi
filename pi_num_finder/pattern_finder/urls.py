from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('search/', views.pi_search, name="pi_search"),
    path('pi/<int:mil_number>/', views.pi_chunk_detail, name='pi_chunk_detail'),
]
