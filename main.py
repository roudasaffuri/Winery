from flask import Flask, render_template, request, redirect, url_for, flash, session
from Tips import get_wine_tips
from addItem import addItemToDB
from context_processors import inject_current_year
from db_connection import disconnection, create_connection
from deleteProduct import deleteItemFromDB
from getWineById import getWineById
from sentMessage import sentMessage
from registration import registration
from login import log
from store import wines
from getProductByID import get_wine_by_id
from userUpdateCart import userUpdateCart
from updateProduct import updateProduct
from dotenv import load_dotenv
import os
from sendUserPassword import sendPass
from clearSessionAndLogout import exitAndClearSession
from ageVerified import ageVerified
from decimal import Decimal

from userCart import getCart

load_dotenv()

KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = KEY  # Replace with a strong secret key for production


# Register the context processor
app.context_processor(inject_current_year)


#---------------------- Index / Login / Signup / Reset ------------------------#
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return ageVerified()
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return log()
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return registration()
    return render_template('signup.html')  # Render the signup form



@app.route('/sendPasswordToEmail', methods=['GET', 'POST'])
def sendPasswordToEmail():
    if request.method == 'POST':
        userEmail = request.form['email']
        sendPass(userEmail)
    return redirect(url_for('login'))


#-------------------------------- USER  ---------------------------------#

@app.route('/home')
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tips")
def tips():
    return render_template("tips.html")


# @app.route("/cart")
# def cart():
#     return render_template("cart.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST" :
        data = request.form
        sentMessage(data)
        return render_template("contact.html", msg_sent=True) # Redirect to avoid form resubmission
    return render_template("contact.html", msg_sent=False)


@app.route("/tipsPage")
def tipsPage():
    return render_template("tipsPage.html",tips=get_wine_tips())


@app.route('/store',)
def store():
    return render_template('store.html', all_wines=wines())


@app.route('/singlePage/<int:id>')
def singlePage(id):
    return getWineById(id)

@app.route('/history')
def history():
    return render_template("history.html")
#-------------------------------- ADD TO CART  ---------------------------------#





@app.route('/cart')
def cart():
    return getCart()
    return render_template("cart.html")




@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove a product from the user's cart."""
    conn = create_connection()
    try:
        cur = conn.cursor()

        # Get cart_id
        user_id = session.get('id')
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        cart_row = cur.fetchone()

        cart_id = cart_row[0]

        # Delete item
        cur.execute(
            "DELETE FROM cart_items WHERE cart_id = %s AND wine_id = %s",
            (cart_id, product_id)
        )
        conn.commit()
        flash("Item removed from cart.")
    except Exception as e:
        flash("Error removing item from cart.")
    finally:
        if cur:
            disconnection(conn, cur)

    # Redirect back to where the user came from
    return redirect(request.referrer or url_for('singlePage', id=product_id))


@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    cart_item_id = request.form.get('cart_item_id')
    action = request.form.get('action')

    if not cart_item_id or action not in ['increase', 'decrease']:
        flash("Invalid update request.")
        return redirect(url_for('cart'))

    conn = create_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ci.quantity, w.stock 
            FROM cart_items ci 
            JOIN wines w ON ci.wine_id = w.id 
            WHERE ci.cart_item_id = %s
        """, (cart_item_id,))
        row = cur.fetchone()

        if row:
            quantity, stock = row

            if action == 'increase' and quantity < stock:
                cur.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE cart_item_id = %s", (cart_item_id,))
            elif action == 'decrease' and quantity > 1:
                cur.execute("UPDATE cart_items SET quantity = quantity - 1 WHERE cart_item_id = %s", (cart_item_id,))
            else:
                flash("Quantity limit reached.")
            conn.commit()
        else:
            flash("Item not found.")
    except Exception as e:
        print(f"Update error: {e}")
        flash("Failed to update quantity.")
    finally:
        if cur:
            disconnection(conn, cur)

    return redirect(url_for('cart'))








# Route to add an item to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'], endpoint='add_to_cart')
def add_to_cart(product_id):
    # If accessed via GET, redirect back to the product page
    if request.method == 'GET':
        flash("Invalid access method for adding to cart.")
        return redirect(request.referrer or url_for('singlePage', id=product_id))

    useremail = session.get('useremail')
    if not useremail:
        flash("Please log in to add items to your cart.")
        return redirect(url_for('login'))

    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    wine = get_wine_by_id(product_id)
    if not wine:
        flash("Product not found.")
        return redirect(url_for('store'))
    if wine.stock < quantity:
        flash("Insufficient stock!")
        return redirect(request.referrer or url_for('singlePage', id=product_id))

    conn = create_connection()
    cur = conn.cursor()
    try:
        # Get user id
        cur.execute("SELECT id FROM users WHERE email = %s", (useremail,))
        result = cur.fetchone()
        if not result:
            flash("User not found.")
            return redirect(url_for('login'))
        user_id = result[0]

        # Get or create cart
        cur.execute("SELECT cart_id FROM carts WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            cart_id = row[0]
        else:
            cur.execute(
                "INSERT INTO carts (user_id, created_at, updated_at) VALUES (%s, NOW(), NOW()) RETURNING cart_id",
                (user_id,)
            )
            cart_id = cur.fetchone()[0]
            conn.commit()

        # Add or update cart_item
        cur.execute(
            "SELECT cart_item_id, quantity FROM cart_items WHERE cart_id = %s AND wine_id = %s",
            (cart_id, product_id)
        )
        item = cur.fetchone()
        if item:
            cart_item_id, existing_qty = item
            new_qty = existing_qty + quantity
            cur.execute(
                "UPDATE cart_items SET quantity = %s, price_at_addition = %s, added_at = NOW() WHERE cart_item_id = %s",
                (new_qty, wine.price, cart_item_id)
            )
        else:
            cur.execute(
                "INSERT INTO cart_items (cart_id, wine_id, quantity, price_at_addition, added_at) VALUES (%s, %s, %s, %s, NOW())",
                (cart_id, product_id, quantity, wine.price)
            )
        conn.commit()
        flash(f"{wine.wine_name} added to cart!")
    except Exception as e:
        conn.rollback()
        flash("Error adding product to cart.")
        print(f"Error in add_to_cart: {e}")
    finally:
        cur.close()
        conn.close()

    # Redirect back to the product detail page
    return redirect(request.referrer or url_for('singlePage', id=product_id))

from flask import request, redirect, url_for, flash, session
from db_connection import create_connection, disconnection



#-------------------------------------------------------------------------------#


#-------------------------------- Admin  ---------------------------------#

@app.route('/admin')
def admin():
    wines = wines()
    return render_template('admin.html', all_wines=wines)


@app.route('/addProduct')
def addProduct():
    return render_template('addProduct.html')

@app.route('/add-wine', methods=['POST'])
def add_wine():
    if request.method == 'POST':
        wine_name = request.form['wineName']
        wine_price = request.form['winePrice']
        wine_quantity = request.form['wineQuantity']
        wine_image = request.form['wineImage']
        return addItemToDB(wine_name,wine_price,wine_quantity,wine_image)


@app.route('/edit-product', methods=['POST'])
def edit_product():
    item_id = request.form.get('itemId')  # Get the itemId from the form data
    print(f"Received item_id: {item_id}")  # Debug output
    wine_details = get_wine_by_id(item_id)  # Fetch wine details using item_id
    if wine_details is None:
        flash("Wine not found.", "danger")
        return redirect(url_for('admin'))  # Redirect if not found

    return render_template('editProduct.html', wine=wine_details)


@app.route('/up', methods=['GET', 'POST'])
def up():
    if request.method == 'POST':
        item_id = request.form['itemId']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        image = request.form['image']

        return updateProduct(item_id,name,price,quantity,image)

    # Handle the GET request
    return render_template('edit_product.html')  # You may want to pass item_id for pre-filling data


@app.route('/delete-wine', methods=['POST'])
def delete_wine():
    if request.method == 'POST':
        item_id = request.form['itemId']
        return deleteItemFromDB(item_id)


#------------------------------- Logout User and Admin --------------------------------#

@app.route('/logout')
def logout():
    return exitAndClearSession()


if __name__ == "__main__":
    app.run(debug=True)
