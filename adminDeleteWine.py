from flask import redirect, url_for, flash, render_template

from adminGetAllWines import getAllWines
from db_connection import create_connection

def deleteItemFromDB(item_id):
    conn = create_connection()
    cur = conn.cursor()

    # SQL delete query
    sql = "DELETE FROM wines WHERE id = %s;"

    try:
        # Execute the delete query
        cur.execute(sql, (item_id,))
        conn.commit()
        flash('Wine deleted successfully!', 'success')  # Flash success message
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while deleting the wine.', 'danger')  # Flash error message
    finally:
        conn.close()

    return render_template('adminManageProducts.html', all_wines=getAllWines())