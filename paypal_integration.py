# paypal_integration.py
import os
from flask import redirect, url_for, flash, session, request, current_app as app
import paypalrestsdk
from complete_order import complete_order

# Configure PayPal SDK once
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

def start_paypal_payment(total):
    """
    Create a PayPal payment and redirect the user to the approval URL.
    """
    username = session.get('username')

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('paypal_execute', _external=True),
            "cancel_url": url_for('userCart', _external=True)
        },
        "transactions": [{
            "amount": {"total": f"{total:.2f}", "currency": "USD"},
            "description": f"Order for user {username}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                return redirect(link.href)
        flash("Approval URL not found.", "error")
    else:
        app.logger.error("Error creating PayPal payment: %s", payment.error)
        flash("Error creating PayPal payment.", "error")
    return redirect(url_for('userHomePage'))


def finalize_paypal_payment():
    """
    Finalize an approved PayPal payment after the user returns from PayPal.
    """
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    if not payment_id or not payer_id:
        flash("Missing payment information.", "error")
        return redirect(url_for('cart'))

    payment = paypalrestsdk.Payment.find(payment_id)

    if not payment.execute({"payer_id": payer_id}):
        app.logger.error("PayPal execute failed: %s", payment.error)
        flash("Payment execution failed. Please try again.", "error")
        return redirect(url_for('cart'))

    return complete_order()
