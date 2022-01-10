from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = '__all__'


