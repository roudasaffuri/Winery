import paypalrestsdk
from flask import session, url_for, redirect, flash

from db_connection import create_connection


def paypalPayment(total):
    conn = create_connection()
    username = session.get('username')
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('paypal_execute', _external=True),
            "cancel_url": url_for('cart', _external=True)
        },
        "transactions": [{
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD"
            },
            "description": f"Order for user {username}"
        }]
    })
    # payment.create() sends your request to PayPal and returns True if the resource was created successfully.
    if payment.create():
        for link in payment.links:
            print(link.href)
            if link.rel == 'approval_url':
                return redirect(link.href)
        flash("Approval URL not found.")
    else:
        flash("Error creating PayPal payment.")
    conn.close()
    return redirect(url_for('home'))