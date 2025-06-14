from flask import redirect, url_for, request, flash
from db_connection import create_connection,disconnection
from psycopg2 import sql
from fernet_encryption import encode_string
import base64

def registration():
    firstname = request.form['firstname']  # Get firstname
    lastname = request.form['lastname']  # Get lastname
    email = request.form['email']  # Get email
    password = request.form['password']  # Get password
    birth_year = request.form['birthyear']  # Get birth year
    gender = request.form['gender']  # Get gender


    # Encrypt and encode the password
    password_encrypt = encode_string(password)
    password_encrypt_base64 = base64.b64encode(password_encrypt).decode('utf-8')

    conn = create_connection()
    cur = conn.cursor()
    try:
        # Insert data into the users table
        insert_query = sql.SQL(
            "INSERT INTO users (firstname, lastname, email, password, birth_year, gender) VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cur.execute(insert_query, (firstname, lastname, email, password_encrypt_base64, birth_year, gender))
        conn.commit()
        flash('Your registration has been successfully', 'success')
        return redirect(url_for('login'))  # Redirect to the home page after successful signup

    except Exception as e:
        print(f"Error: {e}")
        disconnection(conn,cur)
        flash('An unexpected error occurred during signup. Please try again.', 'danger')
        flash('If you\'ve already signed up, please try logging in.', 'info')  # Suggestive, less accusatory
        return redirect(url_for('login'))
