from decimal import Decimal, ROUND_HALF_UP
from flask import request
from ClassWine import Wine
from db_connection import create_connection, disconnection

def calculate_discounted_price(wine):
    price_dec = Decimal(wine.price)
    discount_dec = Decimal(wine.discount)
    hundred = Decimal('100')
    new_price = ((hundred - discount_dec) / hundred) * price_dec
    return new_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def getAllWines():
    search = request.args.get('search', '').strip()
    sort_by_stock = request.args.get('sort_by_stock')  # will be "1" if checkbox is checked

    conn = create_connection()
    cursor = conn.cursor()

    try:
        wines = []
        base_query = "SELECT * FROM wines"
        conditions = []
        params = []

        if search:
            conditions.append("""
                (
                    CAST(id AS TEXT) ILIKE %s OR
                    wine_name ILIKE %s OR
                    wine_type ILIKE %s
                )
            """)
            like_pattern = f"%{search}%"
            params.extend([like_pattern, like_pattern, like_pattern])

        # Add WHERE clause if conditions exist
        if conditions:
            base_query += " WHERE "+"".join(conditions)


        # Add ORDER BY
        if sort_by_stock:
            base_query += " ORDER BY stock ASC"
        else:
            base_query += " ORDER BY id ASC"

        cursor.execute(base_query, tuple(params))
        result = cursor.fetchall()

        for row in result:
            wine = Wine(*row)

            # row[9] = discount
            if int(row[9]) != 0:
                wine.final_price = calculate_discounted_price(wine)

            wines.append(wine)

        return wines

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        disconnection(conn, cursor)
