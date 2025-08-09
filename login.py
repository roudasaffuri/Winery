from db_connection import create_connection, disconnection
from flask import redirect, url_for, flash, session, request, render_template
from fernet_encryption import decode_string
import  base64


def log_in():
    if request.method == 'POST':

        useremail = request.form['email']
        password = request.form['password']

        conn = create_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                # Check if the username (email) exists in the database
                # and also fetch the password,isAdmin and firstname.
                cur.execute("SELECT  id, password, role_id , firstname , lastname ,is_blocked FROM users WHERE email = %s", (useremail,))
                result = cur.fetchone()

                if result is not None:

                    id, stored_password_base64, role_id, firstname, lastname, is_blocked = result

                    if is_blocked :
                        flash("email blocked by admin ",'danger')
                        return render_template('login.html')

                    # Decode the stored password from base64
                    stored_password = base64.b64decode(stored_password_base64)
                    decrypted_password = decode_string(stored_password)

                    # Verify the password
                    if decrypted_password == password:
                        session['id'] = id
                        session['username'] = firstname
                        session['lastname'] = lastname
                        session['useremail'] = useremail

                        # Set session and redirect based on role
                        if role_id == 2:  # Admin
                            session['admin'] = useremail
                            return redirect(url_for('adminManageProducts'))
                        elif role_id == 3:  # Manager
                            session['admin'] = useremail
                            session['manager'] = useremail
                            return redirect(url_for('adminManageProducts'))
                        else:
                            return redirect(url_for('userHomePage'))  # Regular user

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
    else:
        return render_template("login.html")