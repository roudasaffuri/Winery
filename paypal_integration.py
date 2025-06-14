import os
import paypalrestsdk
from flask import url_for

# Configure once on import
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

def create_paypal_payment(user_id, total_amount):
    """Create a PayPal payment and return the approval URL."""
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('paypal_execute', _external=True),
            "cancel_url": url_for('userCreditCardCheckout', _external=True)
        },
        "transactions": [{
            "amount": {"total": f"{total_amount:.2f}", "currency": "USD"},
            "description": f"Order for user {user_id}"
        }]
    })


    # find the approval_url
    for link in payment.links:
        if link.rel == 'approval_url':
            return link.href
    return None

def execute_paypal_payment(payment_id, payer_id):
    """Execute an approved payment. Returns True on success."""
    payment = paypalrestsdk.Payment.find(payment_id)
    return payment.execute({"payer_id": payer_id})
