from ClassWine import Wine
from db_connection import create_connection, disconnection
from decimal import Decimal  # לדיוק בחישוב

def getWineById(id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = "SELECT * FROM wines WHERE id = %s;"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        print(result)

        if result is None:
            return "Product not found", 404


        wine = Wine(
            id=result[0],
            wine_name=result[1],
            wine_type=result[2],
            image_url=result[3],
            price=result[4],
            stock=result[5],
            description=result[6],
            best_before=result[7],
            product_registration_date=result[8],
            discount=result[9],
            final_price=result[10]
        )

        return wine

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Internal Server Error", 500

    finally:
        disconnection(conn, cursor)
