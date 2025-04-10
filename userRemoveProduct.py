from flask import session, flash
from db_connection import create_connection, disconnection


def removeProduct(product_id):
    conn = create_connection()
    try:
        cur = conn.cursor()

        # Get cart_id
        user_id = session.get('id')
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart_row = cur.fetchone()

        cart_id = cart_row[0]

        # Delete item
        cur.execute(
            "DELETE FROM cart_items WHERE cart_id = %s AND wine_id = %s",
            (cart_id, product_id)
        )
        conn.commit()
        flash("Item removed from cart.")
    except Exception as e:
        flash("Error removing item from cart.")
    finally:
        disconnection(conn, cur)

