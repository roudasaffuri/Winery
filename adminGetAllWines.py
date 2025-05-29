from decimal import Decimal, ROUND_HALF_UP
from ClassWine import Wine
from db_connection import create_connection, disconnection

def getAllWines():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM public.wines ORDER BY id ASC")
        result = cursor.fetchall()  # Fetch all rows
        wines = []

        for row in result:


            wine = Wine(*row)

            if int(row[9]) == 0:
                wines.append(wine)
            else:
                price_dec = Decimal(wine.price)
                discount_dec = Decimal(wine.discount)
                hundred = Decimal('100')

                new_price = ((hundred - discount_dec) / hundred) * price_dec
                new_price = new_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                wine.price = new_price

                wines.append(wine)

        return wines
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        disconnection(conn, cursor)


