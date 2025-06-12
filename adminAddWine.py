from flask import flash, render_template, request

from adminGetAllWines import getAllWines
from db_connection import create_connection

def addWine():
    wine_name = request.form['wineName']
    wine_type = request.form['wineType']
    wine_price = request.form['winePrice']
    wine_quantity = request.form['wineQuantity']
    wine_description = request.form['wineDescription']
    wine_best_before = request.form['wineBestBefore']
    wine_image = request.form['wineImage'] or 'https://bravofarms.com/cdn/shop/products/red-wine.jpg?v=1646253890'


    conn = create_connection()
    cur = conn.cursor()

    # SQL insert query
    sql = """
            INSERT INTO wines (wine_name, wine_type,image_url, price,  stock ,description,best_before,final_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

    try:
        # Execute the insert query
        cur.execute(sql, (wine_name, wine_type,wine_image, wine_price,  wine_quantity,wine_description, wine_best_before ,wine_price))
        conn.commit()
        flash('Wine added successfully!', 'success')  # Flash success message
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while adding the wine.', 'danger')  # Flash error message
    finally:
        conn.close()

    return render_template('adminManageProducts.html', all_wines=getAllWines())