from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User


class SignUpForm(UserCreationForm):
    """For for signing up."""

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """For for signing in."""
    class Meta:
        model = User
        fields = '__all__'


