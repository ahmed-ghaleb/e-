# core/urls.py
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="home"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    path("login/",  RedirectView.as_view(url="/accounts/login/",  permanent=False)),
    path("logout/", RedirectView.as_view(url="/accounts/logout/", permanent=False)),

    path("rds/", include("rds.urls")),
]
