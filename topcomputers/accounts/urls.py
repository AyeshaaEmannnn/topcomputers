from django.urls import path
from .views import signup_page, login_page, signup_user, login_user, logout_user

urlpatterns = [
    # signup routes intentionally left out – registration is disabled
    path("login/", login_page, name="login_page"),
    path("logout/", logout_user, name="logout"),

    # form submit urls
    path("login/submit/", login_user, name="login_user"),
    # signup/submit/ not exposed
]
