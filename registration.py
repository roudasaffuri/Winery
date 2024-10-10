from flask import redirect, url_for
from db_connection import create_connection,disconnection
from psycopg2 import sql
import hashlib

def registration(firstname, lastname, email, password):
    # Encode the data to bytes
    encoded_data = password.encode('utf-8')

    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(encoded_data)

    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()

    conn = create_connection()
    cur = conn.cursor()
    try:
        # Insert data into the users table
        insert_query = sql.SQL("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)")
        cur.execute(insert_query, (firstname, lastname, email, hash_hex))
        conn.commit()
        disconnection(conn,cur)

        return redirect(url_for('index'))  # Redirect to a success page
    except Exception as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()
        return "There was an error during signup", 500