from ClassWine import Wine
from db_connection import create_connection, disconnection

def getAllWines():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM public.wines ORDER BY id ASC")
        result = cursor.fetchall()  # Fetch all rows
        wines=[]
        for row in result:
            wine = Wine(*row)  # Unpack row into Wine constructor
            wines.append(wine)
            print(wine)

        return wines
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        disconnection(conn, cursor)



