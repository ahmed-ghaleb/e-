# accounts/views.py
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@method_decorator([sensitive_post_parameters(), csrf_protect, never_cache], name='dispatch')
class LoginView(auth_views.LoginView):
    """
    Custom login view for e& Egypt employees.
    Uses PRG (Post → Redirect → Get) on both success and failure so
    error messages don't persist on refresh.
    """
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('core:dashboard')

    def get_success_url(self):
        return reverse_lazy('core:dashboard')

    def form_valid(self, form):
        # Successful login → message + redirect (handled by parent)
        username = form.cleaned_data.get('username')
        messages.success(
            self.request,
            f'Welcome back, {username}! You have successfully logged in to e& Egypt Self-Service Portal.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Failed login → add a single message and redirect back to the login page
        (PRG) so refresh won't resubmit the POST or re-show errors.
        """
        messages.error(
            self.request,
            'Invalid username or password. Please check your credentials and try again.'
        )
        return redirect('accounts:login')  # PRG on failure

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)


class LogoutView(auth_views.LogoutView):
    """
    Custom logout view.
    """
    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(
                request,
                'You have been successfully logged out from e& Egypt Self-Service Portal.'
            )
        return super().dispatch(request, *args, **kwargs)
