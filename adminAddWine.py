from flask import redirect, url_for, flash, render_template

from adminGetAllWines import getAllWines
from db_connection import create_connection

def addItemToDB(
            wine_name,
            wine_type,
            wine_price,
            wine_quantity,
            wine_description,
            wine_best_before,
            wine_image
        ):
    conn = create_connection()
    cur = conn.cursor()

    # SQL insert query
    sql = """
            INSERT INTO wines (wine_name, wine_type,image_url, price,  stock ,description,best_before)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """

    try:
        # Execute the insert query
        cur.execute(sql, (wine_name, wine_type,wine_image,wine_price,  wine_quantity,wine_description,wine_best_before))
        conn.commit()
        flash('Wine added successfully!', 'success')  # Flash success message
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while adding the wine.', 'danger')  # Flash error message
    finally:
        conn.close()

    return render_template('adminManageProducts.html', all_wines=getAllWines())