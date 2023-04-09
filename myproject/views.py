from datetime import datetime
import pyotp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import send_otp


def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            send_otp(request)
            request.session['username'] = username
            return redirect('otp')
        else:
            error_message = "Invalid username or password"
    return render(request, 'login.html', {'error_message': error_message})

def otp_view(request):
    error_messahe = None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_time = request.session['otp_valid_time']

        if otp_secret_key and otp_valid_time is not None:
            valid = datetime.fromisoformat(otp_valid_time)
            if valid > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_time']

                    return redirect('main')
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass
    return render(request, 'otp.html', {})

@login_required
def main_view(request):
    return render(request, 'main.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')