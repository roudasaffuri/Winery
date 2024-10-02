import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

OWN_PASSWORD_PG = os.getenv("OWN_PASSWORD_PG")
def create_connection():
    """Create a database connection."""
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password=OWN_PASSWORD_PG,
        port=5432
    )

def disconnection(conn, cur):
    """Close the database cursor and connection."""
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


##------------------------------------------------------------------#
####"""Create the USERS table."""####

# conn = create_connection()
# if conn is not None:
#     try:
#         cur = conn.cursor()
#         cur.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id SERIAL PRIMARY KEY,
#                 firstname VARCHAR(100) NOT NULL,
#                 lastname VARCHAR(100) NOT NULL,
#                 email VARCHAR(100) UNIQUE NOT NULL,
#                 password VARCHAR(255) NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         conn.commit()
#     except Exception as e:
#         print(f"Error creating table: {e}")
#     finally:
#         disconnection(conn, cur)

##------------------------------------------------------------------#

# conn = create_connection()
# if conn is not None:
#     try:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users")  # Use correct SQL syntax
#         all_users = cur.fetchall()  # Fetch all results
#         for user in all_users:
#             print(user)  # Print each user
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         cur.close()  # Ensure cursor is closed
#         conn.close()  # Ensure connection is closed

##------------------------------------------------------------------#


####"""Create the tblproducts table."""####

# conn = create_connection()
# if conn is not None:
#     try:
#         cur = conn.cursor()
#         # Create items table
#         cur.execute('''
#             CREATE TABLE IF NOT EXISTS tblproducts (
#                 itemId SERIAL PRIMARY KEY,
#                 itemName VARCHAR(255) NOT NULL,
#                 itemPrice DECIMAL(10, 2) NOT NULL,
#                 itemImgUrl TEXT NOT NULL,
#                 itemCount INT NOT NULL
#             )
#         ''')
#         conn.commit()
#         print("Table 'tblproducts' created successfully.")
#     except Exception as e:
#         print(f"Error creating table: {e}")
#     finally:
#         disconnection(conn, cur)


##------------------------------------------------------------------#


# ####"""to insert multiple items into tblproducts"""####
#
# conn = create_connection()
# if conn is not None:
#     try:
#         cur = conn.cursor()
#
#         # Optionally reset the sequence to start from 1 (if table is empty)
#         cur.execute("ALTER SEQUENCE tblproducts_itemid_seq RESTART WITH 1;")
#
#         # List of items to insert
#         items = [
#             ("Macallan 18 Year Old", 50, "https://img.thewhiskyexchange.com/700/macob.18yov1...", 0),
#             ("Jura 18 Year Old", 400, "https://img.thewhiskyexchange.com/700/iojob.18yov2...", 18),
#             ("Ballantine's 21 Year Old", 550, "https://img.thewhiskyexchange.com/700/blend_bal21y...", 32),
#             ("Glenfiddich 15 Year Old Solera", 150, "https://img.thewhiskyexchange.com/700/gfdob.15yo.j...", 29),
#             ("Chivas Regal 12 Year Old", 550, "https://img.thewhiskyexchange.com/700/blend_chi5.j...", 17),
#             ("Chivas Regal 12", 20, "https://img.thewhiskyexchange.com/700/blend_chi1.j...", 94),
#             ("The Exceptional Grain Third Ed", 180, "https://img.thewhiskyexchange.com/700/grain_exc1.j...", 44),
#             ("Macallan 12 Year Old Triple Cask", 400, "https://img.thewhiskyexchange.com/700/macob.12yov3...", 8),
#             ("Johnnie Walker Blue Label Ghost", 60, "https://img.thewhiskyexchange.com/700/blend_joh230...", 0),
#         ]
#
#         # Insert each item
#         for item in items:
#             cur.execute('''
#                     INSERT INTO tblproducts (itemName, itemPrice, itemImgUrl, itemCount)
#                     VALUES (%s, %s, %s, %s)
#                 ''', item)
#
#         conn.commit()
#         print("Items inserted successfully.")
#     except Exception as e:
#         print(f"Error inserting items: {e}")
#     finally:
#         disconnection(conn, cur)