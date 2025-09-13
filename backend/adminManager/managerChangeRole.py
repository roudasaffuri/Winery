from flask import redirect, url_for, request, flash
from backend.server.db_connection import create_connection, disconnection


def changeRole():
    user_id = request.form['user_id']
    new_role_id = request.form['role_id']

    conn = create_connection()
    cur = conn.cursor()

    # עדכון התפקיד
    cur.execute("UPDATE users SET role_id = %s WHERE id = %s", (new_role_id, user_id))
    conn.commit()

    # שליפת שם המשתמש
    cur.execute("SELECT firstname FROM users WHERE id = %s", (user_id,))
    result = cur.fetchone()
    firstname = result[0]

    disconnection(conn, cur)

    flash(f"Role ID for user '{firstname}' was successfully updated.", 'success')
    return redirect(url_for('managerManageAdmins'))
