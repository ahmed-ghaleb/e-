# core/views.py
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

# Reuse the dummy-session key from accounts so we're checking the same flag
from accounts.views import SESSION_KEY


def _require_dummy_login(request):
    """
    Redirect to the login page if the dummy 'auth' session key is missing.
    Returns a redirect response or None (if allowed).
    """
    if not request.session.get(SESSION_KEY):
        messages.info(request, "Please log in to continue.")
        return redirect("accounts:login")
    return None


def dashboard_view(request):
    """
    Dashboard for the dummy-authenticated user.
    Shows simple RDS stats if the RDS app/model is present.
    Robust to models/fields not existing yet during early prototyping.
    """
    # Must be "logged in" via dummy session
    gate = _require_dummy_login(request)
    if gate:
        return gate

    username = request.session.get(SESSION_KEY)
    now = timezone.now()

    # Default context
    context = {
        "page_title": "Dashboard",
        "username": username,  # request.user isn't used with dummy auth
        "current_time": now,
        "total_instances": 0,
        "running_instances": 0,
        "recent_instances": [],
        "has_rds_data": False,
    }

    # Best-effort RDS stats (handle missing app/model/fields gracefully)
    try:
        from rds.models import RDSInstance  # Imported here to avoid hard dependency

        qs = RDSInstance.objects.all()

        # If model tracks creator, try to scope by dummy username (FK or CharField)
        try:
            if hasattr(RDSInstance, "created_by"):
                try:
                    qs = qs.filter(created_by__username=username)  # FK(User) case
                except Exception:
                    qs = qs.filter(created_by=username)            # CharField case
        except Exception:
            pass

        # Totals
        total_instances = qs.count()

        # Running (if 'status' exists)
        try:
            running_instances = qs.filter(status="available").count()
        except Exception:
            running_instances = 0

        # Recent (if 'created_at' exists)
        try:
            week_ago = now - timedelta(days=7)
            recent_instances = qs.filter(created_at__gte=week_ago).order_by("-created_at")[:5]
        except Exception:
            recent_instances = []

        context.update({
            "total_instances": total_instances,
            "running_instances": running_instances,
            "recent_instances": recent_instances,
            "has_rds_data": True,
        })
    except Exception:
        # rds app/model missing — keep defaults
        pass

    # One-time welcome toast per browser session
    if not request.session.get("welcomed", False):
        messages.success(request, f"Welcome to e& Egypt Self-Service Portal, {username}!")
        request.session["welcomed"] = True

    return render(request, "core/dashboard.html", context)


# Optional: keep the old name working if any URL still points to `views.dashboard`
dashboard = dashboard_view
