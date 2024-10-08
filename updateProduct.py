from flask import redirect, url_for, flash
from db_connection import create_connection

def updateProduct(item_id, name, price, quantity, image):
    conn = create_connection()
    cur = conn.cursor()

    # SQL update query for PostgreSQL
    sql = """
    UPDATE tblproducts
    SET 
        itemName = %s, 
        itemPrice = %s, 
        itemImgUrl = %s, 
        itemCount = %s
    WHERE 
        itemId = %s;
    """

    try:
        # Debugging: print the SQL statement
        print("Executing SQL:", cur.mogrify(sql, (name, price, image, quantity, item_id)))
        cur.execute(sql, (name, price, image, quantity, item_id))
        conn.commit()
        flash('Product updated successfully!', 'success')  # Flash success message
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while updating the product.', 'danger')  # Flash error message
    finally:
        conn.close()

    return redirect(url_for('admin'))  # Make sure to return the redirect here
