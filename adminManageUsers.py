from flask import request, render_template

from db_connection import create_connection ,disconnection


def manageUsers():

    search = request.args.get('search', '').strip()

    conn = create_connection()
    cur = conn.cursor()
    if search:
        query = """
                       SELECT id, firstname, lastname, email, birth_year,
                              gender, role_id, created_at, is_blocked
                       FROM users
                       WHERE role_id = 1 AND (
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
                    SELECT id, firstname, lastname, email, birth_year,
                            gender, role_id, created_at, is_blocked
                             FROM users
                            WHERE role_id = 1
                            ORDER BY id ASC;
                        """)
    users = cur.fetchall()

    disconnection(conn,cur)

    return render_template('adminManageUsers.html', users=users)
