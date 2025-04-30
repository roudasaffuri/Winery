from flask import render_template, session
from db_connection import create_connection, disconnection


def getPurchaseHistory():
    conn = create_connection()
    cursor = conn.cursor()

    # שלוף את כל הרכישות של המשתמש
    cursor.execute("SELECT * FROM purchases WHERE user_id = %s", (session['id'],))
    purchases = cursor.fetchall()

    history_data = []

    for purchase in purchases:
        purchase_id = purchase[0]

        # שלוף פריטים עבור כל רכישה
        cursor.execute("""
                SELECT wine_name, quantity, price_at_purchase, subtotal
                FROM purchase_items
                WHERE purchase_id = %s
            """, (purchase_id,))
        items = cursor.fetchall()

        item_list = []
        for item in items:
            item_dict = {
                'wine_name': item[0],
                'quantity': item[1],
                'price_at_purchase': item[2],
                'subtotal': item[3]
            }
            item_list.append(item_dict)

        purchase_dict = {
            'purchase_id': purchase[0],
            'user_id': purchase[1],
            'total_amount': purchase[2],
            'shipping_price': purchase[3],
            'tax': purchase[4],
            'purchased_at': purchase[5],
            'items': item_list
        }

        history_data.append(purchase_dict)

    disconnection(conn, cursor)

    return render_template('history.html', purchases=history_data)