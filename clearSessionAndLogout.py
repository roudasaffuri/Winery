from flask import session, flash, redirect, url_for

def exitAndClearSession():
    session.clear()  # Clear the user session
    flash("You have been logged out.", "info")  # Flash a logout message
    return redirect(url_for('index'))  # Redirect to the home page
