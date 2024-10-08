from db_connection import create_connection,disconnection

def get_wine_by_id(item_id):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tblproducts WHERE itemId = %s", (item_id,))
            return cur.fetchone()
    except Exception as e:
        print(f"Error fetching wine: {e}")
        return None
    finally:
        disconnection(conn, cur)

print(get_wine_by_id(1))


