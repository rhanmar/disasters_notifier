from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from users.forms import LoginForm, SignUpForm
import os


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    """View to signing up."""
    template_name = "users/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy('main_page')
    success_message = "Registered!"


class UserLoginView(SuccessMessageMixin, LoginView):
    """View to signing in."""
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('main_page')
    success_message = "Logged in!"


class LinkToTelegramView(LoginRequiredMixin, SuccessMessageMixin, generic.TemplateView):
    """View to link Telegram account and User."""
    template_name = "users/link_to_telegram.html"
    success_url = reverse_lazy('main_page')
    success_message = "Successfully linked!"

    def get_context_data(self, **kwargs):
        bot_username = os.getenv("TELEGRAM_BOT_USERNAME")
        link = f"https://telegram.me/{bot_username}?start={self.request.user.id}"
        kwargs['link'] = link
        return super().get_context_data(**kwargs)

