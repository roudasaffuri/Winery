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


def get_wine_by_id(item_id):
    """Fetch wine details using itemId from the tblproducts."""
    conn = create_connection()
    cur = None
    wine_details = None
    try:
        cur = conn.cursor()
        # Fetch wine details
        cur.execute("SELECT * FROM wines WHERE itemId = %s", (item_id,))
        wine_details = cur.fetchone()  # Get one record
    except Exception as e:
        print(f"Error fetching wine details: {e}")
    finally:
        disconnection(conn, cur)

    return wine_details