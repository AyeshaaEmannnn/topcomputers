from django.urls import path
from .views import signup_page, login_page, signup_user, login_user, logout_user

urlpatterns = [
    path("signup/", signup_page, name="signup_page"),
    path("login/", login_page, name="login_page"),
    path("logout/", logout_user, name="logout"),

    # form submit urls
    path("signup/submit/", signup_user, name="signup_user"),
    path("login/submit/", login_user, name="login_user"),
]
