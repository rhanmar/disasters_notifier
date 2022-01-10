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


class LinkToTelegramView(SuccessMessageMixin, generic.TemplateView):
    template_name = "users/link_to_telegram.html"
    success_url = reverse_lazy('main_page')
    success_message = "Successfully linked!"

    def get_context_data(self, **kwargs):
        current_user_unique_code = self.request.user.unique_code
        link = f"https://telegram.me/DimasUsernameBot?start={current_user_unique_code}"  # TODO
        kwargs['link'] = link
        return super().get_context_data(**kwargs)

