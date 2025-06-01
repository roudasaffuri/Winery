from db_connection import create_connection ,disconnection


def updateWineInStock(quantity,wine_id):
    #  clear the cart
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
                        UPDATE wines
                        SET stock = stock - %s
                        WHERE id = %s
                    """, (quantity, wine_id))

    disconnection(conn,cursor)