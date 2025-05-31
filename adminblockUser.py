from flask import redirect, url_for

from db_connection import create_connection,disconnection


def blockUser(user_id,is_blocked):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_blocked = %s WHERE id = %s", (is_blocked, user_id))
    conn.commit()
    disconnection(conn,cur)


    return redirect(url_for('adminManageUsers'))