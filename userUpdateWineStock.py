from db_connection import create_connection ,disconnection


def updateWineInStock(cursor,quantity,wine_id):
    #  clear the cart
    cursor.execute("""
                        UPDATE wines
                        SET stock = stock - %s
                        WHERE id = %s
                    """, (quantity, wine_id))
