from flask import session
from ClassWine import Wine
from collections import Counter
from datetime import datetime
from db_connection import create_connection, disconnection

# Define a Wine class to structure the data


def wines():
    # Create database connection
    conn = create_connection()
    cursor = conn.cursor()
    user_id = session.get('id')



    try:
        # Retrieve the selected user from the database
        user_get_sql = "SELECT * FROM users WHERE id = %s"
        cursor.execute(user_get_sql, (user_id,))
        result = cursor.fetchall()

        # Extract birth year and gender
        birth_year = result[0][5]  # Assuming birth_year is at index 5
        user_gender = (result[0][6]).title()  # Assuming gender is at index 6 and capitalizing it

        # Calculate the user's age
        current_year = datetime.now().year
        user_age = current_year - birth_year
        print(f"User Age: {user_age}, Gender: {user_gender}")

        # Select users of similar age and same gender
        if user_age < 25:
            sql = "SELECT id FROM users WHERE birth_year BETWEEN %s AND %s AND gender = %s;"
            cursor.execute(sql, (current_year - 25, current_year - 18, user_gender))
        elif user_age > 65:
            sql = "SELECT id FROM users WHERE birth_year BETWEEN %s AND %s AND gender = %s;"
            cursor.execute(sql, (current_year - 80, current_year - 60, user_gender))
        else:
            age_min = user_age - 5
            age_max = user_age + 5
            sql = "SELECT id FROM users WHERE birth_year BETWEEN %s AND %s AND gender = %s;"
            cursor.execute(sql, (current_year - age_max, current_year - age_min, user_gender))

        # Fetch users within the same age range
        results = cursor.fetchall()
        print(f"Total users in the same age group: {len(results)}")
        # print(results)

        # Extract user IDs
        list_id_users = [row[0] for row in results]
        print(f"User IDs in the same age group: {list_id_users}")

        # Get purchase IDs for each user
        list_purchase_id = []
        for id in list_id_users:
            sql = "SELECT purchase_id FROM purchases WHERE user_id = %s;"
            cursor.execute(sql, (int(id),))
            results = cursor.fetchall()
            list_purchase_id.extend([row[0] for row in results])

        print(f"Purchase IDs from the 'purchases' table: {list_purchase_id}")

        # Get wine IDs from purchase items
        wines_popular = []
        for purchase_id in list_purchase_id:
            sql = "SELECT wine_id FROM purchase_items WHERE purchase_id = %s;"
            cursor.execute(sql, (int(purchase_id),))
            results = cursor.fetchall()
            wines_popular.extend([row[0] for row in results])

        print(f"Wine IDs from the 'purchase_items' table: {wines_popular}")

        # Count frequency of each wine_id
        counter = Counter(wines_popular)

        # Get list of (wine_id, frequency), sorted from most to least frequent
        sorted_items = counter.most_common()
        # Example: [(14, 9), (49, 8), (51, 8), (57, 8), (60, 8), (12, 7), (17, 7), ...]

        # Extract only the unique wine IDs, sorted by popularity
        sorted_unique_wine_ids = [item[0] for item in sorted_items]
        print(f"Sorted unique wine IDs by popularity: {sorted_unique_wine_ids}")

        # Add missing wine IDs (1 to 60) that were not in the list
        for i in range(1, 41):
            if i not in sorted_unique_wine_ids:
                sorted_unique_wine_ids.append(i)

        print(f"Final list of wine IDs (popular first, then missing ones): {sorted_unique_wine_ids}")

        wines = []  # Array to store wine objects

        # Execute the SQL query to select all records from wines
        cursor.execute("SELECT * FROM wines")

        # Fetch all results
        rows = cursor.fetchall()

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

        final_sorted_wine = []
        for id in sorted_unique_wine_ids:
            for wine in wines:
                if wine.id == id:
                    final_sorted_wine.append(wine)

        print(f"the finale sorted wine to send to store.html {final_sorted_wine}")

        return final_sorted_wine


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and database connection
        disconnection(conn, cursor)



