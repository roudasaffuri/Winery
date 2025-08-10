from flask import request, render_template
from db_connection import create_connection ,disconnection

def getAllUsers():

    search = request.args.get('search', '').strip()

    conn = create_connection()
    cur = conn.cursor()
    if search:
        query = """
            SELECT id, firstname, lastname, email, role_id
            FROM users
            WHERE (
                CAST(id AS TEXT) ILIKE %s
                OR firstname ILIKE %s
                OR lastname ILIKE %s
            )
            ORDER BY id ASC;
        """

        like_pattern = f"%{search}%"
        cur.execute(query, (like_pattern, like_pattern, like_pattern))
    else:
        cur.execute("""
            SELECT id, firstname, lastname, email, role_id
            FROM users ORDER BY id ASC;
        """)

    users = cur.fetchall()

    disconnection(conn,cur)

    return render_template('managerManageAdmins.html', users=users)