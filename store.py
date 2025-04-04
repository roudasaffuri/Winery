from db_connection import create_connection, disconnection
from Wine import Wine
# Define a Wine class to structure the data



def wines():
    # Create a connection to the database
    conn = create_connection()
    cur = conn.cursor()

    wines = []  # Array to store wine objects

    try:
        # Execute the SQL query to select all records from wines
        cur.execute("SELECT * FROM wines")

        # Fetch all results
        rows = cur.fetchall()

        # Map each row to a Wine object and append to the wines list
        for row in rows:
            wine = Wine(
                id=row[0],
                wine_name=row[1],
                wine_type=row[2],
                image_url=row[3],
                price=row[4],
                stock=row[5],
                description=row[6],
                best_before=row[7],
                product_registration_date=row[8]
            )
            wines.append(wine)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        disconnection(conn, cur)

    return wines



