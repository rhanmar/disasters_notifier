from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('sign-up/', views.UserRegisterView.as_view(), name="sign_up"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
