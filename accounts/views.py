# accounts/views.py
from django import forms
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

# ---------- Dummy credentials ----------
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "pass"

# Session key marking a dummy "logged-in" user
SESSION_KEY = "dummy_user"


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def _is_dummy_authenticated(request) -> bool:
    return bool(request.session.get(SESSION_KEY))


def _login_dummy(request, username: str) -> None:
    request.session[SESSION_KEY] = username
    # "Remember me" support (optional):
    if request.POST.get("remember"):
        request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
    else:
        request.session.set_expiry(0)  # expire on browser close


def _logout_dummy(request) -> None:
    request.session.pop(SESSION_KEY, None)


@method_decorator([sensitive_post_parameters(), csrf_protect, never_cache], name="dispatch")
class LoginView(View):
    """
    Dummy login that checks static credentials.
    If already logged in via dummy session, redirect to dashboard.
    """
    template_name = "accounts/login.html"
    success_url = reverse_lazy("dashboard")

    def get(self, request):
        # If you want to ALWAYS show the form even when logged in, comment the next 3 lines.
        if _is_dummy_authenticated(request):
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        # If user somehow already logged in, just send them on.
        if _is_dummy_authenticated(request):
            return redirect(self.success_url)

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if username == DEMO_USERNAME and password == DEMO_PASSWORD:
                # Make sure any Django-auth session is cleared (e.g., from /admin)
                django_logout(request)
                _login_dummy(request, username)
                messages.success(
                    request,
                    f"Welcome back, {username}! You have successfully logged in to e& Egypt Self-Service Portal."
                )
                return redirect(self.success_url)

        messages.error(
            request,
            "Invalid username or password. Please check your credentials and try again."
        )
        return redirect("accounts:login")


@method_decorator([never_cache], name="dispatch")
class LogoutView(View):
    """
    Clears both dummy-session login and any Django-auth login.
    Accepts GET for convenience while prototyping.
    """
    next_page = reverse_lazy("accounts:login")

    def get(self, request):
        # Clear both auth mechanisms
        _logout_dummy(request)
        django_logout(request)
        messages.info(request, "You have been logged out.")
        return redirect(self.next_page)

    def post(self, request):
        _logout_dummy(request)
        django_logout(request)
        messages.info(request, "You have been logged out.")
        return redirect(self.next_page)
