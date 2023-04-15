from datetime import datetime
import pyotp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import send_otp

# function to log in user
def login_view(request):
    error_message = None                                                        # declare a variable for error message
    if request.method == "POST":                                                # if request from front end is POST
        username = request.POST['username']                                     # get username from submitted form
        password = request.POST['password']                                     # get password from submitted form
        user = authenticate(request, username=username, password=password)      # verify user credentials
        if user is not None:                                                    # if credentials were authenticated
            send_otp(request)                                                   # call function that generates one time passcode
            request.session['username'] = username                              # store username in current user session
            return redirect('otp')                                              # redirect to the page to enter otp
        else:                                                                   # if user credentials were not authenticated
            error_message = "Invalid username or password"                      # assign an error message
    return render(request, 'login.html', {'error_message': error_message})      # render response

#function to authenticate otp 
def otp_view(request):
    error_message = None                                                        # declare a variable for error message
    if request.method == 'POST':                                                # if request from front end is POST
        otp = request.POST['otp']                                               # get otp from submitted form
        username = request.session['username']                                  # get username from current user session

        otp_secret_key = request.session['otp_secret_key']                      # get secret key from current user session
        otp_valid_time = request.session['otp_valid_time']                      # get time from current user session

        if otp_secret_key and otp_valid_time is not None:                       # if secret key and time are obtained
            valid = datetime.fromisoformat(otp_valid_time)                      # convert time into datetime object and store in valid
            if valid > datetime.now():                                          # if valid time is greater than current time
                totp = pyotp.TOTP(otp_secret_key, interval=60)                  # generate time-based one-time passwords valid for 60 seconds
                if totp.verify(otp):                                            # if otp from user is valid
                    user = get_object_or_404(User, username=username)           # etrieve an object from the database 
                    login(request, user)                                        # create a user sessiom
                    del request.session['otp_secret_key']                       # delete otp from session storage
                    del request.session['otp_valid_time']                       # delete time from session storage

                    return redirect('main')                                     # redirect to main page
                else:                                                           # if otp is not valid
                    error_message = "Invalid one time password"                 # generate an error message
            else:                                                               # if time is not valid
                error_message = "One time password has expired"                 # generate an error message
        else:                                                                   # if either secret key or time are not obtained
            error_message = "Something went wrong."                             # generate an error message

    return render(request, 'otp.html', {'error_message': error_message})        # render the page

@login_required                                                                 # decorator to mark functions that requir user authentication
def main_view(request):
    return render(request, 'main.html', {})                                     # render main page after log in

def logout_view(request):
    logout(request)                                                             # log out 
    return redirect('login')                                                    # redirect to log in page