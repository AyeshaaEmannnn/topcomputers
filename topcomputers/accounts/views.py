from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User

def signup_page(request):
    # signup disabled – redirect users to login with a message
    from django.contrib import messages
    messages.info(request, "Signup has been disabled. Please contact the administrator.")
    return redirect("login_page")


def signup_user(request):
    # block any attempt to create a user; signup is no longer available
    from django.contrib import messages
    messages.error(request, "User registration is currently disabled.")
    return redirect("login_page")


def login_page(request):
    return render(request, "login.html")


def login_user(request):
    if request.method == "POST":
        email_or_username = request.POST.get("username")
        password = request.POST.get("password")

        # Try to authenticate with email or username
        user = authenticate(username=email_or_username, password=password)
        
        # If not found, try to find by email
        if user is None:
            try:
                user_by_email = User.objects.get(email=email_or_username)
                user = authenticate(username=user_by_email.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            messages.error(request, "Invalid email/username or password!")
            return redirect("login_page")

        # only staff members may access through this login
        if not user.is_staff:
            messages.error(request, "Only administrator accounts can log in here.")
            return redirect("login_page")

        login(request, user)
        messages.success(request, "Login Successful!")
        return redirect("/home/")

    return redirect("login_page")


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login_page")
