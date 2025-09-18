from flask import Flask, render_template, g
from backend.server.ClassTips import get_wine_tips
from backend.adminManager.adminAddWine import addWine
from backend.adminManager.managerChangeRole import changeRole
from backend.adminManager.adminDiscountWineById import discountWine
from backend.adminManager.adminEditProduct import adminEditProduct
from backend.adminManager.adminGetAllWines import getAllWines
from backend.adminManager.adminManageUsers import getRegularUsers
from backend.adminManager.adminStatisticWine import viewStatisticByIdWine
from backend.adminManager.adminUpdateWine import updateWine
from backend.adminManager.adminblockUser import blockUser
from backend.server.complete_order import complete_order
from backend.server.context_processors import inject_context
from backend.adminManager.adminDeleteWine import deleteWineFromDB
from backend.user.userGetSinglePage import userGetSinglePage
from backend.adminManager.managerManageAdmins import getAllUsers
from backend.server.paypal_integration import start_paypal_payment, finalize_paypal_payment
from backend.user.userItemsInCart import get_cart_count
from backend.user.userPaymentByCard import PaymentByCard
from backend.user.userPurchseHistory import getPurchaseHistory
from backend.user.userSentMessage import contactUs
from backend.server.registration import registration
from backend.server.login import log_in
from backend.user.userStore import getStorePage
from backend.user.userSendUserPassword import sendPass
from backend.server.clearSessionAndLogout import exitAndClearSession
from backend.user.userAgeVerified import userAgeVerified
from backend.user.userAddToCart import handle_add_to_cart
from backend.user.userCart import getCart
from backend.user.userRemoveProduct import removeProductFromCart
from backend.user.userUpdateQuantity import handle_quantity_update
import os
from dotenv import load_dotenv
load_dotenv()


KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = KEY  # Replace with a strong secret key for production

# Register the context processor
app.context_processor(inject_context)


# - - - - - - - - - - - - - - Index / Login / Signup / Reset - - - - - - - - - - - - - - #
@app.route('/', methods=['GET', 'POST'])
def index():
    return userAgeVerified()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return log_in()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return registration()


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('PrivacyPolicy.html')


@app.route('/sendPasswordToEmail', methods=['GET', 'POST'])
def sendPasswordToEmail():
    return sendPass()

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
    return userGetSinglePage(id)


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
    return start_paypal_payment(total)

@app.route('/paypal_execute')
def paypal_execute():
    return finalize_paypal_payment()

# Credit Card
@app.route('/userCreditCardCheckout')
def userCreditCardCheckout():
    return PaymentByCard()


@app.route('/process_payment_credit_card', methods=['POST'])
def process_payment_credit_card():
    return complete_order()


# - - - - - - - - - - - - - - Admin  - - - - - - - - - - - - - - #
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
    return getRegularUsers()


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
    return getAllUsers()


@app.route('/changeRole', methods=['POST'])
def change_role():
    return changeRole()


# - - - - - - - - - - - - - - Logout User and Admin Manager - - - - - - - - - - - - - - #
@app.route('/logout')
def logout():
    return exitAndClearSession()


if __name__ == "__main__":
    app.run(debug=True)
