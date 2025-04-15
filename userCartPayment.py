from _decimal import Decimal
from flask import session, redirect, url_for
from db_connection import create_connection
from userClearTheCart import clearTheCart
from userUpdateWineStock import updateWineInStock


def paymentCart():
    user_id = session.get('id')
    conn = create_connection()
    cursor = conn.cursor()

    # 1. Fetch cart items for this user
    cursor.execute("""
                SELECT ci.cart_item_id, ci.wine_id, ci.quantity, ci.price_at_addition,
                       w.wine_name, w.stock
                FROM cart_items ci
                JOIN carts c ON ci.cart_id = c.cart_id
                JOIN wines w ON ci.wine_id = w.id
                WHERE c.user_id = %s
            """, (user_id,))
    cart_items = cursor.fetchall()

    subtotal = Decimal('0.00')
    for item in cart_items:
        _, _, quantity, price_at_addition, _, _ = item
        subtotal += Decimal(price_at_addition) * quantity

    # 2. Calculate shipping, tax, total
    shipping = Decimal('0.00') if subtotal > 50 else Decimal('20.00')
    tax = subtotal * Decimal('0.10')
    total = subtotal + shipping + tax

    # 3. Insert into purchases table
    cursor.execute("""
                INSERT INTO purchases (user_id, total_amount, shipping_price, tax)
                VALUES (%s, %s, %s, %s)
                RETURNING purchase_id
            """, (user_id, total, shipping, tax))
    purchase_id = cursor.fetchone()[0]

    # 4. Insert into purchase_items for each item
    for item in cart_items:
        cart_item_id, wine_id, quantity, price_at_addition, wine_name, stock = item
        subtotal_item = Decimal(price_at_addition) * quantity

        cursor.execute("""
                    INSERT INTO purchase_items (purchase_id, wine_id, wine_name, quantity, price_at_purchase, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (purchase_id, wine_id, wine_name, quantity, price_at_addition, subtotal_item))

        # 5. Update wine stock
        updateWineInStock(quantity,wine_id)


    # 6.  Clear the cart
    clearTheCart(user_id)

    conn.commit()
    conn.close()

    print("Purchase processed and saved.")
    return redirect(url_for('home'))