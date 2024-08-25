from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from myproject import settings
from .forms import userRegisterform, userLoginForm, ResetPasswordForm, ForgetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str


def home(request):
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = userRegisterform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = userRegisterform()
    return render(request, 'accounts/register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = userLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login_success')
            else:
                messages.error(request, f'Invalid username or password')
    else:
        form = userLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def login_success(request):
    return render(request, 'accounts/login_success.html')


def logoutView(request):
    logout(request)
    return redirect('login')


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                # Generate reset link
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    f'/reset_password/{uid}/{token}/')

                # Send reset link via email
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Password reset link sent')
                return redirect('login')
            else:
                messages.error(request, 'No user found with this email')
    else:
        form = ForgetPasswordForm()

    return render(request, 'accounts/forget_password.html', {'form': form})


def reset_password(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Password reset successfully')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match')
        else:
            form = ResetPasswordForm()
        return render(request, 'accounts/reset_password.html', {'form': form})
    else:
        messages.error(request, 'Invalid reset link')
        return redirect('forget_password')
