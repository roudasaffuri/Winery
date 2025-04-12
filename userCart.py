from _pydecimal import Decimal
from flask import session, flash, render_template, redirect, url_for
from db_connection import create_connection, disconnection


def getCart():

    conn = create_connection()
    cur = None
    cart_items = []
    try:
        cur = conn.cursor()
        user_id = session.get('id')

        # Get cart_id
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart_row = cur.fetchone()
        if cart_row:
            cart_id = cart_row[0]
            query = """
                   SELECT ci.cart_item_id,
                          ci.quantity,
                          ci.price_at_addition,
                          w.id,           
                          w.wine_name,
                          w.image_url,
                          w.stock
                   FROM cart_items ci
                   JOIN wines w ON ci.wine_id = w.id
                   WHERE ci.cart_id = %s
               """
            cur.execute(query, (cart_id,))
            for cart_item_id, quantity, price_at_addition, wine_id, wine_name, image_url, stock in cur.fetchall():
                # אם הכמות בעגלה גדולה מהמלאי
                if quantity > stock:
                    flash(
                        f"Only {stock} left in stock for {wine_name}. Requested {quantity}, so the product wasn't added to your cart.")
                    # נמחק את הפריט מהעגלה, או נאפס את הכמות ל־stock, לפי מדיניות
                    quantity = stock
                    cur.execute(
                        "UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s",
                        (stock, cart_item_id)
                    )
                    conn.commit()

                total = Decimal(quantity) * Decimal(str(price_at_addition))
                cart_items.append({
                    "cart_item_id": cart_item_id,
                    "quantity": quantity,
                    "price": price_at_addition,
                    "id": wine_id,
                    "name": wine_name,
                    "image": image_url,
                    "stock": stock,
                    "total": total
                })
    except Exception as e:
        print(f"Cart error: {e}")
    finally:
        if cur:
            disconnection(conn, cur)

    subtotal = sum(item["total"] for item in cart_items)
    tax = subtotal * Decimal('0.1')

    # Shipping logic
    if subtotal < Decimal('50'):
        shipping = Decimal('20.00')
    else:
        shipping = Decimal('0.00')

    total = subtotal + tax + shipping



    return render_template("cart.html",
                           cart_items=cart_items,
                           subtotal=subtotal,
                           tax=tax,
                           shipping=shipping,
                           total=total)

    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal, tax=tax, total=total)