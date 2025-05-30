from flask import flash, redirect, url_for
from db_connection import create_connection ,disconnection


def discountWineById(wine_id , discount) :
    conn = create_connection()
    cursor = conn.cursor()
    sql = "UPDATE wines SET discount = %s WHERE id = %s;"

    cursor.execute(sql, (discount, wine_id))
    conn.commit()
    # print(cursor.rowcount) אם בוצע העדכון בהצלחה מחזיר 1 אחרת 0
    if cursor.rowcount > 0:
        flash("Wine discount updated successfully", "success")
    else:
        flash("No wine found with that ID", "warning")
    disconnection(conn,cursor)
    return redirect(url_for('adminStatistics'))