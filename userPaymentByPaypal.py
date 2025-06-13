import paypalrestsdk
from flask import request, app, flash, redirect, url_for
from complete_order import complete_order
def paymentByPaypal():
    # 1. Grab the PayPal IDs from the query string
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
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