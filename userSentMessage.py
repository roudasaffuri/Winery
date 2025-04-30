from dotenv import load_dotenv
import os
import smtplib
load_dotenv()

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD_EMAIL")



def sentMessage(data):
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    message = data["message"]
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)





