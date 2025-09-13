from flask import session, flash, redirect, url_for, request
from backend.server.db_connection import create_connection



def handle_add_to_cart(product_id):

    quantity = int(request.form.get('quantity', 1))

    wine_name = request.form.get('wine_name')

    conn = create_connection()
    cur = conn.cursor()
    try:

        user_id = session.get('id')

        # Get or create cart
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            # row[0] -> cart_id
            cart_id = row[0]

        else:
            cur.execute(
                "INSERT INTO carts (user_id, created_at, updated_at) VALUES (%s, NOW(), NOW()) RETURNING cart_id",
                (user_id,)
            )
            cart_id = cur.fetchone()[0]
            conn.commit()

        # If exist update cart_item
        cur.execute(
            "SELECT cart_item_id, quantity FROM cart_items WHERE cart_id = %s AND wine_id = %s",
            (cart_id, product_id)
        )
        item = cur.fetchone()
        if item:
            cart_item_id, existing_qty = item
            new_qty = existing_qty + quantity
            cur.execute(
                "UPDATE cart_items SET quantity = %s,  added_at = NOW() WHERE cart_item_id = %s",
                (new_qty, cart_item_id)
            )
        # else Add it to cart_items
        else:
            cur.execute(
                "INSERT INTO cart_items (cart_id, wine_id, quantity, added_at) VALUES (%s, %s, %s, NOW())",
                (cart_id, product_id, quantity)
            )
        conn.commit()
        flash(f"{wine_name} added to cart!" , 'success')
    except Exception as e:
        flash("Error adding product to cart.", 'error')

    finally:
        cur.close()
        conn.close()

    # Redirect back to the product detail page
    return redirect(url_for('userStore'))