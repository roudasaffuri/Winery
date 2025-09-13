from flask import flash, redirect, url_for, request
from backend.server.db_connection import create_connection ,disconnection


def discountWine():
    wine_id = request.form.get('wine_id')
    discount = int(request.form.get('discount'))

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Get current price
        cursor.execute("SELECT price FROM wines WHERE id = %s", (wine_id,))
        price = float(cursor.fetchone()[0])
        # Calculate final price after discount
        final_price = price * ((100 - discount) / 100)
        # Update the wine's discount and final price
        cursor.execute(
            "UPDATE wines SET discount = %s, final_price = %s WHERE id = %s",
            (discount, final_price, wine_id)
        )
        conn.commit()

        flash("Wine discount updated successfully", "success")

    except Exception as e:
        flash(f"Error updating wine discount: {e}", "error")

    finally:
        disconnection(conn, cursor)

    return redirect(url_for('adminManageProducts'))