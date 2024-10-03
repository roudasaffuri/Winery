from wine import get_wines
from sendEmail import send_email, forgetPassword
from dateTimeYear import get_year
from flask import Flask, render_template, request, redirect, url_for, flash, session
from registration import registration
from login import log


app = Flask(__name__)
app.secret_key = 'your_secret_key_I_am_the_big_BOSS'  # Replace with a strong secret key for production

@app.context_processor
def inject_current_year():
    return {'current_year': get_year()}

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']  # Make sure to hash this in production!
        return registration(firstname, lastname, email, password)
    return render_template('signup.html')  # Render the signup form


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
        return render_template("contact.html", msg_sent=True, current_year=get_year()) # Redirect to avoid form resubmission
    return render_template("contact.html", msg_sent=False)


@app.route('/products')
def products():
    return render_template('products.html', all_wines=get_wines())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return log(username,password)


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        username = request.form['email']
        if forgetPassword(username):
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash("Email does not exist. Please try a different email.", "error")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    flash("You have been logged out.", "info")  # Flash a logout message
    return redirect(url_for('index'))  # Redirect to the home page


if __name__ == "__main__":
    app.run(debug=True)
