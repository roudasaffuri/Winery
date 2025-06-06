from flask import request, redirect, url_for, render_template


def ageVerified():
    age_verified = request.form['age_verified']
    if age_verified == 'yes':
        return redirect(url_for('login'))  # שולח לדף ה-login
    else:
        return redirect("https://www.google.com")  # מפנה לגוגל אם המשתמש לא עבר את האימות

def userAgeVerified():
    if request.method == 'POST':
        return ageVerified()
    return render_template("index.html")