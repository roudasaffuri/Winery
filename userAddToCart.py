from flask import session, flash, redirect, url_for
from db_connection import create_connection


def handle_add_to_cart(wine ,quantity ):
    conn = create_connection()
    cur = conn.cursor()
    try:

        user_id = session.get('id')

        # Get or create cart
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            cart_id = row[0]
        else:
            cur.execute(
                "INSERT INTO carts (user_id, created_at, updated_at) VALUES (%s, NOW(), NOW()) RETURNING cart_id",
                (user_id,)
            )
            cart_id = cur.fetchone()[0]
            conn.commit()

        # Add or update cart_item
        cur.execute(
            "SELECT cart_item_id, quantity FROM cart_items WHERE cart_id = %s AND wine_id = %s",
            (cart_id, wine.id)
        )
        item = cur.fetchone()
        if item:
            cart_item_id, existing_qty = item
            new_qty = existing_qty + quantity
            cur.execute(
                "UPDATE cart_items SET quantity = %s, price_at_addition = %s, added_at = NOW() WHERE cart_item_id = %s",
                (new_qty, wine.price, cart_item_id)
            )
        else:
            cur.execute(
                "INSERT INTO cart_items (cart_id, wine_id, quantity, price_at_addition, added_at) VALUES (%s, %s, %s, %s, NOW())",
                (cart_id, wine.id, quantity, wine.price)
            )
        conn.commit()
        flash(f"{wine.wine_name} added to cart!")
    except Exception as e:
        flash("Error adding product to cart.")

    finally:
        cur.close()
        conn.close()

    # Redirect back to the product detail page
    return redirect(url_for('store'))