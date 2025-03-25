from flask import redirect, url_for, flash
from db_connection import create_connection

def addItemToDB(wine_name,wine_price,wine_quantity,wine_image):
    conn = create_connection()
    cur = conn.cursor()

    # SQL insert query
    sql = """
            INSERT INTO tblproducts (itemName, itemPrice, itemImgUrl, itemCount)
            VALUES (%s, %s, %s, %s);
            """

    try:
        # Execute the insert query
        cur.execute(sql, (wine_name, wine_price, wine_image, wine_quantity))
        conn.commit()
        flash('Wine added successfully!', 'success')  # Flash success message
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while adding the wine.', 'danger')  # Flash error message
    finally:
        conn.close()

    return redirect(url_for('admin'))