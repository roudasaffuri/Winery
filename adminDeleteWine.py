from flask import  flash, render_template, request

from adminGetAllWines import getAllWines
from db_connection import create_connection ,disconnection

def deleteWineFromDB():

    item_id = request.form['wineId']

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
        disconnection(conn,cur)

    return render_template('adminManageProducts.html', all_wines=getAllWines())