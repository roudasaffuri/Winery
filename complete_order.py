from decimal import Decimal
from db_connection import create_connection
from userClearTheCart import clearTheCart
from userSendOrderConfirmationEmail import send_order_confirmation_email
from flask import session, flash, redirect, url_for, render_template , g

def complete_order():
    """
    1. Get user id  using session
    2. Fetch cart items for this user
    3. **Check availability**: if any qty > stock, flash + redirect
    4. Calculate subtotal, shipping, tax, total
    5. Insert into purchases & purchase_items
    6. Update wine stock
    7. Clear the cart
    8. Send confirmation email
    9. Update the globle object g.cart_count to 0
    Returns the total amount, or a redirect Response if stock is insufficient.
    """

    user_id = session.get('id')

    conn    = create_connection()
    cursor  = conn.cursor()

    # — 1) Fetch cart items (including current stock) —
    cursor.execute("""
        SELECT ci.cart_item_id, ci.wine_id, ci.quantity, w.final_price,
               w.wine_name, w.stock
          FROM cart_items ci
          JOIN carts c ON ci.cart_id = c.cart_id
          JOIN wines w ON ci.wine_id = w.id
         WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()
    if not cart_items:
        g.cart_count = 0
        return render_template("userCart.html")
    # — 2) Availability check —
    for _, _, qty, _, wine_name, stock in cart_items:
        if stock < qty:
            # Not enough stock for this item
            flash(f"Sorry! only {stock} of “{wine_name}” left in stock. "
                  "Please adjust your cart and try again.", "warning")
            conn.close()
            # return a redirect Response; it has a status_code attribute (e.g. 302 for redirects, 200 for OK)
            return redirect(url_for('userCart'))

    # — 3) Calculate totals —
    subtotal = Decimal('0.00')
    for _, _, qty, price, _, _ in cart_items:
        subtotal += Decimal(price) * qty
    shipping = Decimal('0.00') if subtotal > Decimal('50.00') else Decimal('20.00')
    tax      = subtotal * Decimal('0.10')
    total    = subtotal + shipping + tax

    # — 4) Insert purchase record —
    cursor.execute("""
        INSERT INTO purchases (user_id, total_amount, shipping_price, tax)
             VALUES (%s, %s, %s, %s)
         RETURNING purchase_id
    """, (user_id, total, shipping, tax))
    purchase_id = cursor.fetchone()[0]

    # — 5) Insert items & update stock —
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
    conn.commit()
    # — 6) Clear the cart —
    clearTheCart(user_id)

    # — 7) Send confirmation email —
    summary = {
        "subtotal":      subtotal,
        "shipping_cost": shipping,
        "tax":           tax,
        "total":         total
    }
    if session.get('useremail'):
        send_order_confirmation_email(session['useremail'], summary, purchase_id)
    flash('Purchase successfully! Email sent.', 'success')

    g.cart_count = 0
    return render_template("userCart.html")
