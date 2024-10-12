from db_connection import create_connection, disconnection
from flask import redirect, url_for, flash, session
from fernet_encryption import decode_string
import  base64
def log(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            # Check if the username (email) exists in the database
            cur.execute("SELECT password, isAdmin FROM users WHERE email = %s", (username,))
            result = cur.fetchone()

            if result is not None:
                stored_password_base64, isAdmin = result
                # Decode the stored password from base64
                stored_password = base64.b64decode(stored_password_base64)
                decrypted_password = decode_string(stored_password)

                # Verify the password
                if decrypted_password == password:
                    # Check admin status
                    if username == 'admin@email.com' and isAdmin:
                        session['admin'] = username
                        return redirect(url_for('admin'))
                    session['username'] = username
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
