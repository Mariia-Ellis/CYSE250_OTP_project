import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    #timebased one time password variable to generate a code valid for 60 seconds
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)

    #generate otp
    otp = totp.now()

    request.session['otp_secret_key'] = totp.secret

    #set time for otp to be valid
    valid_time = datetime.now() + timedelta(minutes=1)

    request.session['otp_valid_time'] = str(valid_time)

    print(f"Your one time password is {otp}")