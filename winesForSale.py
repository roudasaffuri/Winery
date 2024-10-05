from db_connection import create_connection, disconnection


def wineForSale():
    # Create a connection to the database
    conn = create_connection()
    cur = conn.cursor()

    try:
        # Execute the SQL query to select all records from tblproducts
        cur.execute("SELECT * FROM tblproducts")

        # Fetch all results
        rows = cur.fetchall()

        # Print the results
        for row in rows:
            print(row)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        disconnection(conn,cur)
    return rows

