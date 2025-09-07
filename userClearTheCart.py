from db_connection import create_connection


def clearTheCart(cursor, user_id):
    cursor.execute("""
        DELETE FROM cart_items
         WHERE cart_id IN (
               SELECT cart_id FROM carts WHERE user_id = %s
         )
    """, (user_id,))