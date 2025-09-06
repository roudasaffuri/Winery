from flask import redirect, url_for, request, flash, render_template
from db_connection import create_connection, disconnection
from psycopg2 import sql, errors
from fernet_encryption import encode_string
import base64

def registration():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        birth_year = request.form['birthyear']
        gender = request.form['gender']

        # Encrypt and encode the password
        password_encrypt = encode_string(password)
        # base64.b64encode   bytes --> bytes64
        # decode('utf-8')   bytes64 --> string
        password_encrypt_base64 = base64.b64encode(password_encrypt).decode('utf-8')

        conn = create_connection()
        cur = conn.cursor()

        try:
            insert_query = sql.SQL(
                "INSERT INTO users (firstname, lastname, email, password, birth_year, gender) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cur.execute(insert_query, (firstname, lastname, email, password_encrypt_base64, birth_year, gender))
            conn.commit()

            flash('Your registration has been successful', 'success')
            return redirect(url_for('login'))

        except errors.UniqueViolation:
            # Roll back the failed transaction
            conn.rollback()
            flash('This email is already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            flash('An unexpected error occurred during signup. Please try again.', 'danger')
            return redirect(url_for('login'))

        finally:
            disconnection(conn, cur)

    else:
        return render_template('signup.html')
