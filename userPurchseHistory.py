from flask import session, render_template
from db_connection import create_connection, disconnection


def getPurchaseHistory():
    conn = create_connection()
    cursor = conn.cursor()

    user_id = session.get('id')

    cursor.execute("SELECT * FROM purchases WHERE user_id = %s", (user_id,))
    purchases = cursor.fetchall()

    history_data = []

    for purchase in purchases:
        purchase_id = purchase[0]

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

    # שימוש ב-render_template
    return render_template("userPurchaseHistory.html", purchases=history_data)
