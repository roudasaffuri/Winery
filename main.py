from flask import Flask, render_template, request, redirect, url_for, g
from Tips import get_wine_tips
from adminAddWine import addWine
from managerChangeRole import changeRole
from adminDiscountWineById import discountWine
from adminEditProduct import  adminEditProduct
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
from userItemsInCart import get_cart_count
from userPaymentByCard import PaymentByCard
from userPaymentByPaypal import paymentByPaypal
from userPurchseHistory import getPurchaseHistory
from userSentMessage import contactUs
from registration import registration
from login import log
from userStore import getStorePage
from dotenv import load_dotenv
from userSendUserPassword import sendPass
from clearSessionAndLogout import exitAndClearSession
from userAgeVerified import  userAgeVerified
from userAddToCart import handle_add_to_cart
from userCart import getCart
from userRemoveProduct import removeProductFromCart
from userUpdateQuantity import handle_quantity_update
import os

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
@app.route('/userHomePage')
def userHomePage():
    return render_template("userHomePage.html")


@app.route("/userContact", methods=["GET", "POST"])
def userContact():
    return contactUs()


@app.route("/userTips")
def userTips():
    return render_template("userTips.html",tips=get_wine_tips())


@app.route('/userStore')
def userStore():
    return getStorePage()



@app.route('/userSinglePage/<int:id>')
def userSinglePage(id):
    best_seller = request.args.get('best_seller', default=0, type=int)
    wine = getWineById(id)
    return render_template("userSinglePage.html", wine=wine, best_seller=best_seller)


@app.route('/userPurchaseHistory')
def userPurchaseHistory():
    return getPurchaseHistory()

#-------------------------------- ADD TO CART  ---------------------------------#
@app.route('/userCart')
def userCart():
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
    return paymentByPaypal()


# Credit Card
@app.route('/userCreditCardCheckout')
def userCreditCardCheckout():
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
    return render_template("adminStatistics.html", all_wines=getAllWines())


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
