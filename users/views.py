from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from users.forms import LoginForm, SignUpForm


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    template_name = "users/sign_up.html"
    # form_class = UserCreationForm
    form_class = SignUpForm
    success_url = reverse_lazy('main_page')
    success_message = "Registered!"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    # form_class = AuthenticationForm
    form_class = LoginForm
    success_url = reverse_lazy('main_page')
    success_message = "Logged in!"


class LinkToTelegramView(LoginRequiredMixin, SuccessMessageMixin, generic.TemplateView):  # TODO login required
    template_name = "users/link_to_telegram.html"
    success_url = reverse_lazy('main_page')
    success_message = "Successfully linked!"

    def get_context_data(self, **kwargs):
        link = f"https://telegram.me/DimasUsernameBot?start={self.request.user.id}"  # TODO move to constant
        kwargs['link'] = link
        return super().get_context_data(**kwargs)

