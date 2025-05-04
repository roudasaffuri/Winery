
from db_connection import create_connection
def get_column_field_names_with_this_query():
    conn = create_connection()
    cur = conn.cursor()

    #table users

    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'users' AND table_schema = 'public';
    """)

    # Fetch and print column names
    columns = cur.fetchall()
    column_names = [col[0] for col in columns]
    print("Columns:", column_names)
    cur.close()
    conn.close()