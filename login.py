from db_connection import create_connection, disconnection
from flask import redirect, url_for, flash, session
import hashlib

def log(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            # Check if the username (email) exists in the database
            cur.execute("SELECT password, isAdmin FROM users WHERE email = %s", (username,))
            result = cur.fetchone()

            if result is not None:
                stored_password, isAdmin = result
                # Encode the password to bytes
                encoded_password = password.encode('utf-8')

                # Create a SHA-256 hash object
                hash_object = hashlib.sha256(encoded_password)

                # Get the hexadecimal representation of the hash
                hash_hex = hash_object.hexdigest()

                # Verify the password
                if stored_password == hash_hex:
                    # Check admin status
                    if username == 'admin@gmail.com' and isAdmin:
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
