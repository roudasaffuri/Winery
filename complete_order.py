from decimal import Decimal
from db_connection import create_connection
from sendOrderConfirmationEmail import send_order_confirmation_email
from flask import session

def complete_order(user_id):
    """
    1. Fetch cart items for this user
    2. Calculate subtotal, shipping, tax, total
    3. Insert into purchases & purchase_items
    4. Update wine stock
    5. Clear the cart
    6. Send confirmation email
    Returns the total amount.
    """
    conn    = create_connection()
    cursor  = conn.cursor()

    # — Fetch cart items —
    cursor.execute("""
        SELECT ci.cart_item_id, ci.wine_id, ci.quantity, ci.price_at_addition,
               w.wine_name, w.stock
          FROM cart_items ci
          JOIN carts c ON ci.cart_id = c.cart_id
          JOIN wines w ON ci.wine_id = w.id
         WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    # — Calculate totals —
    subtotal = Decimal('0.00')
    for _, _, qty, price, _, _ in cart_items:
        subtotal += Decimal(price) * qty
    shipping = Decimal('0.00') if subtotal > Decimal('50.00') else Decimal('20.00')
    tax      = subtotal * Decimal('0.10')
    total    = subtotal + shipping + tax

    # — Insert purchase record —
    cursor.execute("""
        INSERT INTO purchases (user_id, total_amount, shipping_price, tax)
             VALUES (%s, %s, %s, %s)
         RETURNING purchase_id
    """, (user_id, total, shipping, tax))
    purchase_id = cursor.fetchone()[0]

    # — Insert items & update stock —
    for _, wine_id, qty, price, wine_name, _ in cart_items:
        subtotal_item = Decimal(price) * qty
        cursor.execute("""
            INSERT INTO purchase_items
              (purchase_id, wine_id, wine_name, quantity, price_at_purchase, subtotal)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (purchase_id, wine_id, wine_name, qty, price, subtotal_item))

        cursor.execute(
            "UPDATE wines SET stock = stock - %s WHERE id = %s",
            (qty, wine_id)
        )

    # — Clear the cart —
    cursor.execute("""
        DELETE FROM cart_items
        USING carts
        WHERE cart_items.cart_id = carts.cart_id
          AND carts.user_id = %s
    """, (user_id,))

    conn.commit()
    conn.close()

    # — Send confirmation email —
    # build the summary dict, then send
    summary = {
        "subtotal":      subtotal,
        "shipping_cost": shipping,
        "tax":           tax,
        "total":         total
    }
    # assume session['useremail'] is populated
    if session.get('useremail'):
        send_order_confirmation_email(session['useremail'], summary,purchase_id)

    return total
