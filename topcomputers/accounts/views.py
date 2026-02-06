from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User

def signup_page(request):
    return render(request, "signup.html")


def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Generate username from email
        username = email.split('@')[0]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup_page")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup_page")
        
        # Handle username uniqueness
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        try:
            user = User(username=username, email=email, first_name=first_name)
            user.set_password(password)
            user.save()
            messages.success(request, "Signup successful! You can now login.")
            return redirect("login_page")
        except IntegrityError:
            messages.error(request, "Email already registered! Please try with a different email.")
            return redirect("signup_page")

    return redirect("signup_page")


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

        login(request, user)
        messages.success(request, "Login Successful!")
        return redirect("/home/")

    return redirect("login_page")


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login_page")
