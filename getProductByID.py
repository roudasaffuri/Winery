# from db_connection import create_connection, disconnection
# from store import Wine  # Import the Wine class
#
# def get_wine_by_id(id):
#     conn = create_connection()
#     try:
#         with conn.cursor() as cur:
#             # Use the correct column name 'id'
#             cur.execute("SELECT * FROM wines WHERE id = %s", (id,))
#             row = cur.fetchone()
#             if row:
#                 # Map the row to a Wine object
#                 return Wine(
#                     id=row[0],
#                     wine_name=row[1],
#                     wine_type=row[2],
#                     image_url=row[3],
#                     price=row[4],
#                     stock=row[5],
#                     description=row[6],
#                     best_before=row[7],
#                     product_registration_date=row[8]
#
#                 )
#             else:
#                 return None
#     except Exception as e:
#         print(f"Error fetching wine: {e}")
#         return None
#     finally:
#         disconnection(conn, cur)