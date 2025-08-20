# core/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="home"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    path("rds/", include("rds.urls")),
]