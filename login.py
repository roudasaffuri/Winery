from db_connection import create_connection, disconnection
from flask import redirect, url_for, flash, session
from fernet_encryption import decode_string
import  base64
def log(useremail, password):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            # Check if the username (email) exists in the database
            # and also fetch the password,isAdmin and firstname.
            cur.execute("SELECT  password, isAdmin , firstname FROM users WHERE email = %s", (useremail,))
            result = cur.fetchone()

            if result is not None:
                print(result)
                stored_password_base64, isAdmin, firstname = result
                # Decode the stored password from base64
                stored_password = base64.b64decode(stored_password_base64)
                decrypted_password = decode_string(stored_password)

                # Verify the password
                if decrypted_password == password:

                    # Check admin status
                    if useremail == 'admin@email.com' and isAdmin:
                        session['admin'] = useremail
                        return redirect(url_for('admin'))
                    session['username'] = firstname
                    session['useremail']=useremail
                    return redirect(url_for('home'))  # Redirect to a success page
                else:
                    flash("Invalid password", "error")
                    return redirect(url_for('index'))
            else:
                flash("Username not found", "error")
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            disconnection(conn, cur)