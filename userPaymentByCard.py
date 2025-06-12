from flask import session, render_template, g
from _pydecimal import Decimal
from db_connection import create_connection, disconnection

def PaymentByCard():
    user_id = session.get('id')
    cart_items = []
    subtotal = Decimal('0.00')
    tax = Decimal('0.00')
    shipping_cost = Decimal('0.00')
    total = Decimal('0.00')

    if user_id:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart_row = cur.fetchone()
        if not cart_row:
            g.cart_count = 0
            return render_template("cart.html")
        elif cart_row:
            cart_id = cart_row[0]
            query = """
                SELECT ci.cart_item_id,
                       ci.quantity,
                       w.final_price,
                       w.id,
                       w.wine_name
                FROM cart_items ci
                JOIN wines w ON ci.wine_id = w.id
                WHERE ci.cart_id = %s
            """
            cur.execute(query, (cart_id,))
            for cart_item_id, quantity, final_price, wine_id, wine_name in cur.fetchall():
                item_total = Decimal(str(final_price)) * Decimal(quantity)
                cart_items.append({
                    "quantity": quantity,
                    "price": final_price,
                    "name": wine_name,
                    "total": item_total
                })
        disconnection(conn, cur)

        subtotal = sum(item["total"] for item in cart_items)
        tax = subtotal * Decimal('0.1')
        shipping_cost = Decimal('20.00') if subtotal < Decimal('50') else Decimal('0.00')
        total = subtotal + tax + shipping_cost

    return render_template("creditCardCheckout.html",
                           cart_items=cart_items,
                           subtotal=subtotal,
                           shipping_cost=shipping_cost,
                           tax=tax,
                           total=total)
