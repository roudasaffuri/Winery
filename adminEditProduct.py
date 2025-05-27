from flask import render_template

from db_connection import create_connection


def adminEditProduct(wine_id):
    conn = create_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM wines WHERE id = %s;"
    cursor.execute(sql, (wine_id,))
    result = cursor.fetchone()

    if result:
        wine_data = {
            'id': result[0],
            'wine_name': result[1],
            'wine_type': result[2],
            'price': result[4],
            'stock': result[5],
            'year': result[7],
            'image_url': result[3],
            'description': result[6],
        }

        cursor.close()
        conn.close()
        return render_template('adminEditWine.html', wine=wine_data)
    else:
        cursor.close()
        conn.close()
        return "Wine not found", 404