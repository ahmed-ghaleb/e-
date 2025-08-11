# rds/urls.py
from django.urls import path
from . import views

app_name = 'rds'

urlpatterns = [
    path('', views.rds_list, name='list'),
    path('create/', views.rds_create, name='create'),
    path('<int:instance_id>/', views.rds_detail, name='detail'),
    path('<int:instance_id>/delete/', views.rds_delete, name='delete'),
]