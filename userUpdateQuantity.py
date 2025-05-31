from flask import request, redirect, url_for
from db_connection import disconnection, create_connection

def handle_quantity_update():
    cart_item_id = request.form.get('cart_item_id')
    action = request.form.get('action')

    conn = create_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ci.quantity, w.stock 
            FROM cart_items ci 
            JOIN wines w ON ci.wine_id = w.id 
            WHERE ci.cart_item_id = %s
        """, (cart_item_id,))
        row = cur.fetchone()

        if row:
            quantity, stock = row

            if action == 'increase' and quantity < stock:
                cur.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE cart_item_id = %s", (cart_item_id,))
                conn.commit()

            elif action == 'decrease' and quantity > 1:
                cur.execute("UPDATE cart_items SET quantity = quantity - 1 WHERE cart_item_id = %s", (cart_item_id,))
                conn.commit()
            return redirect(url_for('cart'))
    except Exception as e:
        print(f"Update error: {e}")
    finally:
        disconnection(conn, cur)
