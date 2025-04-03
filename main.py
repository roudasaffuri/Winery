from flask import Flask, render_template, request, redirect, url_for, flash
from Tips import get_wine_tips
from addItem import addItemToDB
from context_processors import inject_current_year
from deleteProduct import deleteItemFromDB
from wine1 import get_wines
from sendEmail import send_email
from registration import registration
from login import log
from winesForSale import wineForSale
from getProductByID import get_wine_by_id
from updateProduct import updateProduct
from dotenv import load_dotenv
import os
from resetPassword import resetPass
from clearSessionAndLogout import exitAndClearSession
from ageVerified import ageVerified
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



@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        userEmail = request.form['email']
        if resetPass(userEmail):
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash("Email does not exist. Please try a different email.", "error")
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


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True) # Redirect to avoid form resubmission
    return render_template("contact.html", msg_sent=False)


@app.route('/products')
def products():
    return render_template('products.html', all_wines=get_wines())

@app.route("/tipsPage")
def tipsPage():
    return render_template("tipsPage.html",tips=get_wine_tips())



@app.route('/store',)
def store():
    return render_template('store.html', all_wines=wineForSale())


@app.route('/admin')
def admin():
    wines = wineForSale()
    return render_template('admin.html', all_wines=wines)


@app.route('/addProduct')
def addProduct():
    return render_template('addProduct.html')

@app.route('/singlePage/<int:id>')
def single_page(id):
    wine = get_wine_by_id(id)
    if wine:
        return render_template("singlePage.html", wine=wine)
    else:
        return "Product not found", 404




#-------------------------------- Admin  ---------------------------------#

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
