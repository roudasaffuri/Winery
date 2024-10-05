from db_connection import create_connection,disconnection
from flask import redirect, url_for, flash, session


def log(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            # Check if the username (email) exists in the database
            cur.execute("SELECT password FROM users WHERE email = %s", (username,))
            result = cur.fetchone()

            if result is not None:
                stored_password = result[0]
                # Verify the password directly (not recommended for production)
                if stored_password == password:
                    session['username'] = username
                    if username == 'admin@gmail.com' and password == '123':
                        return redirect(url_for('admin'))
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
