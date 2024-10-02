from flask import redirect, url_for
from db_connection import create_connection,disconnection
from psycopg2 import sql


def registration(firstname, lastname, email, password):
    print(firstname)
    conn = create_connection()
    cur = conn.cursor()
    try:
        # Insert data into the users table
        insert_query = sql.SQL("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)")
        cur.execute(insert_query, (firstname, lastname, email, password))
        conn.commit()
        disconnection(conn,cur)

        return redirect(url_for('index'))  # Redirect to a success page
    except Exception as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()
        return "There was an error during signup", 500