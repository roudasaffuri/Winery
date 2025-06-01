from flask import flash, redirect, url_for, request
from db_connection import create_connection ,disconnection


def discountWine() :
    wine_id = request.form.get('wine_id')
    discount = request.form.get('discount')

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