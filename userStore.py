from flask import session, render_template, flash
from ClassWine import Wine
from collections import Counter
from datetime import datetime,timedelta
from db_connection import create_connection, disconnection


def getStorePage():
    # first10wines() ,get_top5_wines_last_week() and getAllwines() ->Returns a list of objects Wine
    recommendedForYou = first10wines()
    top5_wines = get_top5_wines_last_week()
    allwines = getAllwines()
    return render_template('userStore.html', recommendedForYou=recommendedForYou, top5_wines=top5_wines,all_wines=allwines)


# Define a Wine class to structure the data
def first10wines():
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
        # Select users of similar age and same gender
        if user_age < 25:
            sql = "SELECT id FROM users WHERE birth_year > %s AND gender = %s;"
            cursor.execute(sql, (current_year - 25, user_gender))
        else:
            age_min = user_age - 5
            age_max = user_age + 5
            sql = "SELECT id FROM users WHERE birth_year BETWEEN %s AND %s AND gender = %s;"
            cursor.execute(sql, (current_year - age_max, current_year - age_min, user_gender))

        # Fetch users within the same age range
        results = cursor.fetchall()
        # print(results)

        # Extract user IDs
        list_id_users = [row[0] for row in results]
        # Get purchase IDs for each user
        list_purchase_id = []
        for id in list_id_users:
            sql = "SELECT purchase_id FROM purchases WHERE user_id = %s;"
            cursor.execute(sql, (int(id),))
            results = cursor.fetchall()
            list_purchase_id.extend([row[0] for row in results])

        # Get wine IDs from purchase items
        wines_popular = []
        for purchase_id in list_purchase_id:
            sql = "SELECT wine_id FROM purchase_items WHERE purchase_id = %s;"
            cursor.execute(sql, (int(purchase_id),))
            results = cursor.fetchall()
            wines_popular.extend([row[0] for row in results])
        # Count frequency of each wine_id
        counter = Counter(wines_popular)

        # Get list of (wine_id, frequency), sorted from most to the least frequent
        sorted_items = counter.most_common()
        # print(sorted_items)
        # Example: [(38, 9), (22, 8), (24, 8), (7, 7), (8, 7), (12, 7), (5, 7), (20, 6), (29, 5), ...]
        # slice first 10 items
        sorted_items = sorted_items[:10]
        # Extract only the unique wine IDs, sorted by popularity
        sorted_unique_wine_ids = [item[0] for item in sorted_items]

        first10Wines = []
        for i in range(0, 10):
            sql = "SELECT * FROM wines WHERE id = %s;"
            cursor.execute(sql, (int(sorted_unique_wine_ids[i]),))
            row = cursor.fetchone()
            wine = Wine(
                id=row[0],
                wine_name=row[1],
                wine_type=row[2],
                image_url=row[3],
                price=row[4],
                stock=row[5],
                description=row[6],
                best_before=row[7],
                product_registration_date=row[8],
                discount=row[9],
                final_price=row[10]
            )
            first10Wines.append(wine)
        return first10Wines


    except Exception as e:
        flash(f"Update error: {e}", 'error ')
    finally:
        # Close the cursor and database connection
        disconnection(conn, cursor)

def get_top5_wines_last_week():
    """  מחזיר את 5 היינות הנמכרים ביותר בשבוע האחרון.    """

    try:
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        conn = create_connection()
        cur = conn.cursor()

        # שלב 1 – שליפת כל רכישות השבוע האחרון
        cur.execute("""
            SELECT purchase_id
            FROM purchases
            WHERE purchased_at BETWEEN %s AND %s
        """, (week_ago, now))
        result = cur.fetchall()
        purchase_ids = [row[0] for row in result]

        if not purchase_ids:
            disconnection(conn, cur)
            return []  # אין רכישות בשבוע האחרון

        # שלב 2 – חישוב הכמויות של היינות מתוך הרכישות האלו
        # מחפש בטבלת הpurchase_items
        # purchase_id את כל ה
        cur.execute("""
            SELECT 
                pi.wine_id,
                SUM(pi.quantity) AS total_qty
            FROM purchase_items pi
            WHERE pi.purchase_id = ANY(%s)
            GROUP BY pi.wine_id
            ORDER BY total_qty DESC
            LIMIT 5
        """, (purchase_ids,))
        top_wines_qty = cur.fetchall()
        print(top_wines_qty)
        top5 = []
        for top in top_wines_qty:
            sql = "SELECT * FROM wines WHERE id = %s"
            cur.execute(sql, (top[0],))
            result = cur.fetchone()

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
            top5.append(wine)

        return top5

    except Exception as e:
        print(f"Error in get_top5_wines_last_week: {e}")
        return []

    finally:
        try:
            disconnection(conn, cur)
        except:
            pass


def getAllwines():
    conn = create_connection()
    cursor = conn.cursor()
    getAllWines_sql = "SELECT * FROM wines"
    cursor.execute(getAllWines_sql)
    result = cursor.fetchall()

    allWines = []
    for row in result:
        wine = Wine(
            id=row[0],
            wine_name=row[1],
            wine_type=row[2],
            image_url=row[3],
            price=row[4],
            stock=row[5],
            description=row[6],
            best_before=row[7],
            product_registration_date=row[8],
            discount=row[9],
            final_price=row[10]
        )
        allWines.append(wine)
    return allWines
