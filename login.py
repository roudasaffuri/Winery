import time
from db_connection import create_connection, disconnection
from flask import redirect, url_for, flash, session, request, render_template
from fernet_encryption import decode_string
import  base64

def log():

    useremail = request.form['email']
    password = request.form['password']

    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            # Check if the username (email) exists in the database
            # and also fetch the password,isAdmin and firstname.
            cur.execute("SELECT  id, password, is_admin , firstname FROM users WHERE email = %s", (useremail,))
            result = cur.fetchone()

            if result is not None:
                print(result)
                id, stored_password_base64, is_admin, firstname = result
                # Decode the stored password from base64
                stored_password = base64.b64decode(stored_password_base64)
                decrypted_password = decode_string(stored_password)

                # Verify the password
                if decrypted_password == password:
                    session['id'] = id
                    # Check admin status
                    if useremail == 'admin@email.com' and is_admin:
                        session['admin'] = useremail
                        return redirect(url_for('admin'))
                    session['username'] = firstname
                    session['useremail']=useremail
                    return redirect(url_for('home'))  # Redirect to a success page
                else:
                    flash("Invalid email or password.", "danger")
                    return render_template('login.html')
            else:
                flash("Invalid email or password.", "danger")
                return render_template('login.html')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            disconnection(conn, cur)