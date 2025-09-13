from dotenv import load_dotenv
import os
import smtplib

from flask import request, render_template

load_dotenv()

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD_EMAIL")

def contactUs():
    if request.method == "POST":
        data = request.form
        #ImmutableMultiDict([('name', 'rouda saffuri'), ('email', 'R.saffuri@hotmail.com'), ('phone', '0525676783'), ('message', 'ewersf')])
        sentMessage(data)
        return render_template("userContact.html", msg_sent=True) # Redirect to avoid form resubmission
    return render_template("userContact.html", msg_sent=False)



def sentMessage(data):
    
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    message = data["message"]
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)





