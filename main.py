import paypalrestsdk as paypalrestsdk
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from Tips import get_wine_tips
from adminAddWine import addWine
from managerChangeRole import changeRole
from adminDiscountWineById import discountWine
from adminEditProduct import  adminEditProduct
from adminGenderDistribution import genderDistribution
from adminGetAllWines import getAllWines
from adminManageUsers import manageUsers
from adminStatisticWine import  viewStatisticByIdWine
from adminUpdateWine import updateWine
from adminblockUser import blockUser
from complete_order import complete_order
from context_processors import inject_current_year
from adminDeleteWine import deleteWineFromDB
from getWineById import getWineById
from managerManageAdmins import manageAdmins
from paypalPayment import paypalPayment
from test import seasonalSt
from userItemsInCart import get_cart_count
from userPaymentByCard import PaymentByCard
from userPurchseHistory import getPurchaseHistory
from userSentMessage import contactUs
from registration import registration
from login import log
from userStore import getStorePage
from dotenv import load_dotenv
import os
from userSendUserPassword import sendPass
from clearSessionAndLogout import exitAndClearSession
from userAgeVerified import  userAgeVerified
from userAddToCart import handle_add_to_cart
from userCart import getCart
from userRemoveProduct import removeProductFromCart
from userUpdateQuantity import handle_quantity_update

load_dotenv()

KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = KEY  # Replace with a strong secret key for production

# Register the context processor
app.context_processor(inject_current_year)


# - - - - - - - - - - - - - - Index / Login / Signup / Reset - - - - - - - - - - - - - - #
@app.route('/', methods=['GET', 'POST'])
def index():
    return userAgeVerified()


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

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('PrivacyPolicy.html')


@app.route('/sendPasswordToEmail', methods=['GET', 'POST'])
def sendPasswordToEmail():
    if request.method == 'POST':
        userEmail = request.form['email']
        sendPass(userEmail)
    return redirect(url_for('login'))


# - - - - - - - - - - - - - - USER - - - - - - - - - - - - - - #

@app.route('/home')
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tips")
def tips():
    return render_template("tips.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return contactUs()


@app.route("/tipsPage")
def tipsPage():
    return render_template("tipsPage.html",tips=get_wine_tips())


@app.route('/store')
def store():
    return getStorePage()


@app.route('/singlePage/<int:id>')
def singlePage(id):
    return render_template("singlePage.html", wine=getWineById(id))


@app.route('/history')
def history():
    return getPurchaseHistory()

#-------------------------------- ADD TO CART  ---------------------------------#
@app.route('/cart')
def cart():
    return getCart()


@app.before_request
def load_cart_count():
    g.cart_count = get_cart_count()


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove a product from the user's cart."""
    return removeProductFromCart(product_id)


@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    return handle_quantity_update()


# Route to add an item to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    return handle_add_to_cart(product_id)


# - - - - - - - - - - - - - - PayPal and Credit Card Payment - - - - - - - - - - - - - - #
# Paypal
@app.route('/paypal_payment/<float:total>')
def paypal_payment(total):
    return paypalPayment(total)

@app.route('/paypal_execute')
def paypal_execute():
    # 1. Grab the PayPal IDs from the query string
    payment_id = request.args.get('paymentId')
    payer_id   = request.args.get('PayerID')
    # 2. Look up that payment in the PayPal SDK
    payment = paypalrestsdk.Payment.find(payment_id)
    # 3. Execute it
    if not payment.execute({"payer_id": payer_id}):
        # If execution failed, show an error and send them back
        app.logger.error("PayPal execute failed: %s", payment.error)
        flash("Payment execution failed. Please try again.")
        return redirect(url_for('cart'))
    # 4. On success, run DB+email logic
    return complete_order()


# Credit Card
@app.route('/creditCardCheckout')
def creditCardCheckout():
    return PaymentByCard()

@app.route('/process_payment_credit_card', methods=['POST'])
def process_payment_credit_card():
    return complete_order()



# - - - - - - - - - - - - - - Admin  - - - - - - - - - - - - - - #
@app.route('/adminHomePage')
def adminHomePage():
    return render_template('adminHomePage.html')


@app.route('/adminManageProducts')
def adminManageProducts():
    return render_template('adminManageProducts.html', all_wines=getAllWines())


@app.route('/adminAddProduct')
def adminAddProduct():
    return render_template('adminAddProduct.html')


@app.route('/add-wine', methods=['POST'])
def add_wine():
    return addWine()


@app.route('/delete-wine', methods=['POST'])
def delete_wine():
    return deleteWineFromDB()


@app.route('/edit_product', methods=['POST'])
def edit_product():
    return adminEditProduct()


@app.route('/update_wine', methods=['POST'])
def update_wine():
    return updateWine()


@app.route('/adminManageUsers')
def adminManageUsers():
    return manageUsers()


@app.route('/block_user', methods=['POST'])
def block_user():
    return blockUser()


@app.route('/discountWineById', methods=['POST'])
def discountWineById():
    return discountWine()


@app.route("/adminViewStatistic" , methods=['POST'])
def adminViewStatistic():
    return viewStatisticByIdWine()


@app.route("/adminStatistics")
def adminStatistics():
    gender = genderDistribution()
    male=gender[0]
    female = gender[1]
    return render_template("adminStatistics.html", male=male, female=female , all_wines=getAllWines())


@app.route("/seasonalStatistics")
def seasonalStatistics():
    seasonal_data = seasonalSt()
    return render_template("seasonalStatistics.html", **seasonal_data)


# - - - - - - - - - - - - - - Manager  - - - - - - - - - - - - - - #

@app.route('/managerManageAdmins')
def managerManageAdmins():
    return manageAdmins()


@app.route('/changeRole', methods=['POST'])
def change_role():
    return changeRole()


# - - - - - - - - - - - - - - Logout User and Admin - - - - - - - - - - - - - - #
@app.route('/logout')
def logout():
    return exitAndClearSession()


if __name__ == "__main__":
    app.run(debug=True)
