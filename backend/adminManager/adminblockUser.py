from flask import redirect, url_for, request, flash
from backend.server.db_connection import create_connection,disconnection


def blockUser():
    user_id = request.form.get('user_id')
    # אם ה-checkbox מסומן -> יחזור True
    # אם לא מסומן -> יחזור False
    is_blocked = request.form.get('is_blocked') == 'true'
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_blocked = %s WHERE id = %s", (is_blocked, user_id))
    # get the firstname from the sql to insert in the flash
    cur.execute("SELECT firstname FROM users WHERE id = %s", (user_id,))
    result = cur.fetchone()
    firstname = result[0]
    conn.commit()
    disconnection(conn,cur)
    if is_blocked:
        flash(f"User '{firstname}' has been successfully blocked.", 'danger')
    else:
        flash(f"User '{firstname}' has been successfully activated.", 'success')
    return redirect(url_for('adminManageUsers'))