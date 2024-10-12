from db_connection import create_connection,disconnection
from dotenv import load_dotenv
import os
import smtplib
from fernet_encryption import decode_string
import  base64
load_dotenv()

OWN_EMAIL = "saffuri87@gmail.com"
OWN_PASSWORD = os.getenv("OWN_PASSWORD_EMAIL")



def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


def forgetPassword(username):
    # Establish a database connection
    conn = create_connection()
    cur = conn.cursor()

    try:
        # Fetch the user record based on username
        cur.execute("SELECT email, password FROM users WHERE email = %s;", (username,))
        user = cur.fetchone()

        if user:
            user_email = user[0]
            password = user[1]
            stored_password = base64.b64decode(password)
            decrypted_password = decode_string(stored_password)

            email_message = f"Subject: Password Reset\n\nYour password is: {decrypted_password}\n"

            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(OWN_EMAIL, OWN_PASSWORD)
                connection.sendmail(OWN_EMAIL, user_email, email_message)
                return True
        else:
            print("User not found.")
            return False

    finally:
        # Always close the cursor and connection
        disconnection(conn, cur)


