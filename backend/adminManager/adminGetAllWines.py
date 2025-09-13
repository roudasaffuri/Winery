from decimal import Decimal, ROUND_HALF_UP
from flask import request
from backend.server.ClassWine import Wine
from backend.server.db_connection import create_connection, disconnection


def calculate_discounted_price(wine):
    """Calculate final price after discount (rounded to 2 decimals)."""
    price_dec = Decimal(wine.price)
    discount_dec = Decimal(wine.discount)
    hundred = Decimal('100')

    new_price = ((hundred - discount_dec) / hundred) * price_dec
    return new_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def getAllWines():
    """Fetch all wines with optional search and sorting by stock."""

    # קבלת פרמטרים מה-URL
    search = request.args.get('search', '').strip()
    sort_by_stock = request.args.get('sort_by_stock')  # "1" אם צ'קבוקס מסומן

    conn = create_connection()
    cursor = conn.cursor()

    try:
        wines = []
        params = []

        # בסיס השאילתה
        base_query = "SELECT * FROM wines"

        # חיפוש (WHERE)
        if search:
            base_query += """
                WHERE
                    CAST(id AS TEXT) ILIKE %s
                    OR wine_name ILIKE %s
                    OR wine_type ILIKE %s
            """
            like_pattern = f"%{search}%"
            params = [like_pattern, like_pattern, like_pattern]

        # מיון (ORDER BY)
        if sort_by_stock:
            base_query += " ORDER BY stock ASC"
        else:
            base_query += " ORDER BY id ASC"

        # הרצת השאילתה
        cursor.execute(base_query, tuple(params))
        result = cursor.fetchall()

        # יצירת אובייקטים מסוג Wine
        for row in result:
            wine = Wine(*row)

            # אם יש הנחה - מחשבים מחיר סופי
            if int(row[9]) != 0:
                wine.final_price = calculate_discounted_price(wine)

            wines.append(wine)

        return wines

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        disconnection(conn, cursor)
