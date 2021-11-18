from django.views import generic
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    template_name = "users/sign_up.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('main_page')
    success_message = "Registered!"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('main_page')
    success_message = "Logged in!"


