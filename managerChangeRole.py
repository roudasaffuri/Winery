from flask import redirect, url_for, request
from db_connection import create_connection,disconnection


def changeRole():
    user_id = request.form['user_id']
    new_role_id = request.form['role_id']
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET role_id = %s WHERE id = %s", (new_role_id, user_id))
    conn.commit()

    disconnection(conn,cur)

    return redirect(url_for('managerManageAdmins'))
