import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

OWN_PASSWORD_PG = os.getenv("OWN_PASSWORD_PG")

def create_connection():
    """Create a database connection."""
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password=OWN_PASSWORD_PG,
        port=5432
    )

def disconnection(conn, cur):
    """Close the database cursor and connection."""
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
