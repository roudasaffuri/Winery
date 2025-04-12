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
from updateProduct import updateProduct
from dotenv import load_dotenv
import os
from sendUserPassword import sendPass
from clearSessionAndLogout import exitAndClearSession
from ageVerified import ageVerified
from userAddToCart import handle_add_to_cart

from userCart import getCart
from userRemoveProduct import removeProduct
from userUpdateQuantity import handle_quantity_update

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
    removeProduct(product_id)

    return redirect(url_for('cart'))


@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    cart_item_id = request.form.get('cart_item_id')
    action = request.form.get('action')

    handle_quantity_update(cart_item_id, action)
    return redirect(url_for('cart'))


# Route to add an item to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'], endpoint='add_to_cart')
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    wine = get_wine_by_id(product_id)

    return handle_add_to_cart(wine , quantity)







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
