# CYSE250_OTP_project

clone project from github to your local machine
navigate to project folder and use following commands:

python3 -m venv venv               // command to create a virtual enviroment   
source venv/bin/activate           // command to activate virtual enviroment
pip install django                 // command to install django
pip install pyotp                  // command to install pyotp module for OTP 
pytnon manage.py makemigration     //command to apply changes to database
pytnon manage.py migrate           //command to migrate changes to database
pytnon manage.py runserver         //command to run the server

http://127.0.0.1:8000/             //open in broweser after run server to run the project

One time password is send to terminal and valid for 60 seconds.
