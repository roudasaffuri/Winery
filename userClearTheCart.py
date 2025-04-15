from db_connection import create_connection


def clearTheCart(user_id):
    #  clear the cart
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
                    DELETE FROM cart_items
                    USING carts
                    WHERE cart_items.cart_id = carts.cart_id AND carts.user_id = %s
                """, (user_id,))
    conn.commit()
    conn.close()
