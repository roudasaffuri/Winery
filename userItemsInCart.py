from flask import session
from db_connection import create_connection, disconnection

def get_cart_count():
    """Return total quantity of all items in the current user's cart."""
    conn = create_connection()
    cur = conn.cursor()
    try:
        user_id = session.get('id')
        # find their cart
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if not row:
            return 0
        cart_id = row[0]
        # sum up quantities
        cur.execute("SELECT COALESCE(SUM(quantity),0) FROM cart_items WHERE cart_id = %s", (cart_id,))
        (count,) = cur.fetchone()
        return int(count)
    finally:
        disconnection(conn, cur)