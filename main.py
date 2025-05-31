import paypalrestsdk as paypalrestsdk
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from Tips import get_wine_tips
from adminAddWine import addWine
from adminChangeRole import changeRole
from adminDiscountWineById import discountWineById
from adminEditProduct import  adminEditProduct
from adminGenderDistribution import genderDistribution
from adminGetAllWines import getAllWines
from adminStatisticWine import statisticWine
from adminUpdateWine import updateWine
from adminblockUser import blockUser
from complete_order import complete_order
from context_processors import inject_current_year
from adminDeleteWine import deleteItemFromDB
from db_connection import create_connection
from getWineById import getWineById
from paypalPayment import paypalPayment
from test import seasonalSt
from userPaymentByCard import PaymentByCard
from userPurchseHistory import getPurchaseHistory
from userSentMessage import sentMessage
from registration import registration
from login import log
from store import wines, get_top5_wines_last_week
from dotenv import load_dotenv
import os
from userSendUserPassword import sendPass
from clearSessionAndLogout import exitAndClearSession
from ageVerified import ageVerified
from userAddToCart import handle_add_to_cart
from userCart import getCart, get_cart_count
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

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('PrivacyPolicy.html')


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


@app.route('/store')
def store():
    catalog =wines()
    print(catalog)
    recommended_wines =get_top5_wines_last_week()
    return render_template('store.html',all_wines= catalog,recommended_wines  = recommended_wines)


@app.route('/singlePage/<int:id>')
def singlePage(id):
    print(id)
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
    removeProduct(product_id)

    return redirect(url_for('cart'))


@app.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    return handle_quantity_update()


# Route to add an item to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    return handle_add_to_cart(product_id)



#------------------------------PayPal and Credit Card Payment---------------------------------------#

#Paypal
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
    user_id = session.get('id')
    result = complete_order(user_id)
    # hasattr built-in function that checks whether the object result has an attribute with the given name(status_code).
    #hasattr built-in function that checks whether the object result has an attribute with the given name(status_code).
    if hasattr(result, 'status_code'):
        return result

    total = result
    flash(f"Payment successful! Your order for ${total:.2f} is complete. Email sent.")
    return render_template("cart.html")


# Credit Card
@app.route('/creditCardCheckout')
def creditCardCheckout():
    return PaymentByCard()

@app.route('/process_payment_credit_card', methods=['POST'])
def process_payment_credit_card():
    user_id = session.get('id')
    complete_order(user_id)
    return render_template("cart.html")


    result = complete_order(user_id)
    #hasattr built-in function that checks whether the object result has an attribute with the given name(status_code).
    if hasattr(result, 'status_code'):
        return result
    flash(f"Payment successful! Your order for ${result:.2f} is complete. Email sent.")
    return render_template("cart.html")





#-------------------------------- Admin  ---------------------------------#


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
    if request.method == 'POST':
        item_id = request.form['wineId']
        return deleteItemFromDB(item_id)


@app.route('/edit_product', methods=['POST'])
def edit_product():
    wine_id = request.form.get('id')
    return adminEditProduct(wine_id)



@app.route('/update_wine', methods=['POST'])
def update_wine():
    return updateWine()



@app.route('/adminManageUsers')
def adminManageUsers():

    search = request.args.get('search', '').strip()

    conn = create_connection()
    cur = conn.cursor()
    if search:
        query = """
                   SELECT id, firstname, lastname, email, birth_year,
                          gender, role_id, created_at, is_blocked
                   FROM users
                   WHERE role_id = 1 AND (
                       CAST(id AS TEXT) ILIKE %s
                       OR firstname ILIKE %s
                       OR lastname ILIKE %s
                   )
                   ORDER BY id ASC;
               """
        like_pattern = f"%{search}%"
        cur.execute(query, (like_pattern, like_pattern, like_pattern))
    else:
        cur.execute("""
                SELECT id, firstname, lastname, email, birth_year,
                        gender, role_id, created_at, is_blocked
                         FROM users
                        WHERE role_id = 1
                        ORDER BY id ASC;
                    """)
    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('adminManageUsers.html', users=users)

@app.route('/block_user', methods=['POST'])
def block_user():
    user_id = request.form.get('user_id')
    is_blocked = request.form.get('is_blocked') == 'true'

    return blockUser(user_id,is_blocked)



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


#------------------- Manager -----------------#

@app.route('/managerManageAdmins')
def managerManageAdmins():

    search = request.args.get('search', '').strip()

    conn = create_connection()
    cur = conn.cursor()
    if search:
        query = """
            SELECT id, firstname, lastname, email, role_id
            FROM users
            WHERE (
                CAST(id AS TEXT) ILIKE %s
                OR firstname ILIKE %s
                OR lastname ILIKE %s
            )
            ORDER BY id ASC;
        """

        like_pattern = f"%{search}%"
        cur.execute(query, (like_pattern, like_pattern, like_pattern))
    else:
        cur.execute("""
            SELECT id, firstname, lastname, email, role_id
            FROM users ORDER BY id ASC;
        """)

    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('managerManageAdmins.html', users=users)


@app.route('/changeRole', methods=['POST'])
def change_role():
    user_id = request.form['user_id']
    new_role_id = request.form['role_id']
    return changeRole(user_id , new_role_id)


#------------------------------- Logout User and Admin --------------------------------#
@app.route("/adminChart" , methods=['POST'])
def adminChart():
    wine_id = request.form.get('id')
    labels, data_this_year, data_last_year, std_dev, media , discount = statisticWine(wine_id)
    recommended = round(media + std_dev)

    return render_template("adminChart.html", labels=labels, last_year=data_last_year, this_year=data_this_year,
                       std_dev=round(std_dev), media=round(media), recommended=recommended,discount=discount)


@app.route('/discountByWineId', methods=['POST'])
def discountByWineId():

    wine_id = request.form.get('wine_id')
    discount = request.form.get('discount')

    return discountWineById(wine_id, discount)


@app.route('/logout')
def logout():
    return exitAndClearSession()


if __name__ == "__main__":
    app.run(debug=True)
