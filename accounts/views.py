from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse

# Required when AUTHENTICATION_BACKENDS lists more than one backend.
MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"


def _auth_page_extra_context(request, login_next=None):
    """Safe Google OAuth flags — avoids template calls to provider_login_url without a SocialApp."""
    ctx = {
        "login_next": (login_next if login_next is not None else request.GET.get("next", "")) or "",
        "google_oauth_enabled": False,
        "google_oauth_url": "",
    }
    try:
        from allauth.socialaccount.models import SocialApp

        if SocialApp.objects.filter(provider="google").exists():
            ctx["google_oauth_enabled"] = True
            ctx["google_oauth_url"] = reverse("google_login")
    except Exception:
        pass
    return ctx


def register(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        username = (request.POST.get("username") or email).strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if not username or not password:
            messages.error(request, "Email and password are required")
            return redirect("register")

        if confirm_password and password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        if email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        login(request, user, backend=MODEL_BACKEND)
        messages.success(request, "Account created successfully. Welcome to Yours To Rent.")
        return redirect('owner_dashboard')

    ctx = _auth_page_extra_context(request)
    return render(request, "download/signup.html", ctx)


def user_login(request):
    if request.method == "POST":
        identifier = (request.POST.get("username") or request.POST.get("email") or "").strip()
        password = request.POST.get("password", "")
        username = identifier

        # Support login via either username or email.
        if "@" in identifier:
            user_obj = User.objects.filter(email__iexact=identifier).first()
            if user_obj:
                username = user_obj.username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend=MODEL_BACKEND)
            messages.success(request, "Logged in successfully.")
            next_url = (request.POST.get("next") or request.GET.get("next") or "").strip()
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("owner_dashboard")
        else:
            messages.error(request, "Invalid login details")

    next_val = (request.POST.get("next") or request.GET.get("next") or "").strip()
    ctx = _auth_page_extra_context(request, next_val)
    return render(request, "download/login.html", ctx)


def user_logout(request):
    logout(request)
    return redirect('home')
