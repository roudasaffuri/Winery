from db_connection import create_connection, disconnection

# Define a Wine class to structure the data
class Wine:
    def __init__(self, id, wine_name, wine_type, image_url, price, stock, description, best_before, product_registration_date):
        self.id = id
        self.wine_name = wine_name
        self.wine_type = wine_type
        self.image_url = image_url
        self.price = price
        self.stock = stock
        self.description = description
        self.best_before = best_before
        self.product_registration_date = product_registration_date

    def __repr__(self):
        return f"Wine(id={self.id}, wine_name={self.wine_name}, wine_type={self.wine_type}, price={self.price})"


def wineForSale():
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

# Call the wineForSale function and print the array of wine objects
wines = wineForSale()

# # Print all wine objects
# for wine in wines:
#     print(wine)
