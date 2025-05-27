from datetime import datetime, timedelta

####"""Insert to the purchases & purchase_items table."""####
import pandas as pd
import random
from db_connection import create_connection


from datetime import datetime, timedelta
import random

def random_timestamp_2025():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 8, 31, 23, 59, 59)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)



# יצירת חיבור למסד הנתונים
conn = create_connection()
cur = conn.cursor()

# טען את הקבצים
wines = pd.read_csv("./wines.csv")
users = pd.read_csv("./users.csv")

# בחר משתמש אקראי
for i in range(112,1113):

    user_id = i  # המרה ל-int רגיל

    # בחר 1-3 יינות אקראיים במלאי
    in_stock_wines = wines[wines['stock'] > 0].sample(random.randint(1, 2))

    # בנה את פריטי ההזמנה
    purchase_items_data = []
    subtotal = 0

    for _, row in in_stock_wines.iterrows():
        quantity = random.randint(1, 3)
        price = float(row["price"])
        item_total = price * quantity
        subtotal += item_total

        purchase_items_data.append({
            "wine_id": int(row['id']),
            "wine_name": str(row['wine_name']),
            "quantity": int(quantity),
            "price": price,
            "subtotal": round(item_total, 2)
        })

    # חישוב מס ומשלוח
    tax = round(subtotal * 0.10, 2)
    shipping = 0 if subtotal > 50 else 20
    total = round(subtotal + tax + shipping, 2)
    purchase_date = random_timestamp_2025()
    # SQL ל-purchases
    purchases_sql = """
    INSERT INTO purchases (user_id, total_amount, shipping_price, tax, purchased_at)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING purchase_id;
    """

    cur.execute(purchases_sql, (user_id, total, shipping, tax, purchase_date))
    purchase_id = cur.fetchone()[0]  # קבלת ה-id של ההזמנה

    # SQL ל-purchase_items
    items_sql = """
    INSERT INTO purchase_items (purchase_id, wine_id, wine_name, quantity, price_at_purchase, subtotal)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for item in purchase_items_data:
        cur.execute(items_sql, (
            purchase_id,
            item["wine_id"],
            item["wine_name"],
            item["quantity"],
            item["price"],
            item["subtotal"]
        ))

    # שמירת השינויים
    conn.commit()

    # הדפסה לבדיקה
    print(f"✅ Purchase created for user {user_id} (purchase_id={purchase_id})")
    print("📦 Items purchased:")
    for item in purchase_items_data:
        print(f"  - {item['wine_name']} x{item['quantity']} | {item['subtotal']}₪")
    print(f"\nSubtotal: {round(subtotal, 2)}₪ | Tax: {tax}₪ | Shipping: {shipping}₪ | Total: {total}₪")
