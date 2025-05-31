from flask import request, flash, redirect

from db_connection import create_connection


def updateWine():
    wine_id = request.form.get('itemId')
    name = request.form.get('name')
    wine_type = request.form.get('wine_type')
    price = request.form.get('price')
    stock = request.form.get('stock')
    year = request.form.get('year')
    description = request.form.get('description')
    image_url = request.form.get('image')

    conn = create_connection()
    cursor = conn.cursor()

    sql = '''
        UPDATE wines
        SET wine_name = %s,
            wine_type = %s,
            price = %s,
            stock = %s,
            best_before = %s,
            description = %s,
            image_url = %s
        WHERE id = %s;
        '''
    values = (name, wine_type, price, stock, year, description, image_url, wine_id)
    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()
    flash(f"Wine '{name}' has been successfully updated.", "success")
    return redirect('/adminManageProducts')