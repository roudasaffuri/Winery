import os
import smtplib
from dotenv import load_dotenv
from db_connection import create_connection,disconnection
from email.message import EmailMessage

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD_EMAIL")

load_dotenv()
def send_order_confirmation_email(user_email, order_summary, purchase_id):
    """Send a stylish order confirmation email to customers."""
    subject = "Cheers to Your Exquisite Selection - Online Wine World"

    # Fetch wine details from the database based on purchase_id
    items_list = fetch_wine_details_by_purchase_id(purchase_id)

    # Format the items list into a string
    formatted_items_list = "\n".join([f"• {item['quantity']}x {item['wine_name']} - ${item['price_at_purchase']:.2f}"
                                      for item in items_list])

    # Format the email with HTML for styling

    html_content = f"""
    <html>
    <body style="font-family: 'Garamond', serif; color: #722F37; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #722F37; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">Online Wine World</h1>
            <h2 style="font-style: italic;">Your Order Confirmation</h2>
        </div>

        <p style="font-size: 18px;">Dear Wine Enthusiast,</p>

        <p>Thank you for your exceptional taste and recent purchase from Online Wine World. 
        Your fine selections are being prepared with the utmost care and will be on their way to you shortly.</p>

        <div style="background-color: #F9F5F1; padding: 20px; border-left: 4px solid #722F37; margin: 20px 0;">
            <h3 style="color: #722F37; margin-top: 0;">Order Summary</h3>

            <div style="margin-left: 15px; margin-bottom: 15px;">
                {formatted_items_list if formatted_items_list else "Your selected wines"}
            </div>

            <table style="width: 100%; border-top: 1px solid #D4AF37; padding-top: 10px;">
                <tr>
                    <td style="text-align: right; padding: 5px 0;">Subtotal:</td>
                    <td style="text-align: right; padding: 5px 0;">${order_summary['subtotal']:.2f}</td>
                </tr>
                <tr>
                    <td style="text-align: right; padding: 5px 0;">Shipping:</td>
                    <td style="text-align: right; padding: 5px 0;">${order_summary['shipping_cost']:.2f}</td>
                </tr>
                <tr>
                    <td style="text-align: right; padding: 5px 0;">Tax:</td>
                    <td style="text-align: right; padding: 5px 0;">${order_summary['tax']:.2f}</td>
                </tr>
                <tr style="font-weight: bold; font-size: 18px;">
                    <td style="text-align: right; padding: 10px 0; border-top: 1px solid #D4AF37;">Total:</td>
                    <td style="text-align: right; padding: 10px 0; border-top: 1px solid #D4AF37;">${order_summary['total']:.2f}</td>
                </tr>
            </table>
        </div>

        <p>We recommend allowing your wines to rest for 24-48 hours after delivery before enjoying them at their optimal temperature.</p>

        <div style="font-style: italic; margin: 30px 0; text-align: center; color: #555;">
            "Wine is bottled poetry." — Robert Louis Stevenson
        </div>

        <p style="margin-top: 30px;">With appreciation for your distinguished palate,</p>
        <p style="font-family: 'Brush Script MT', cursive; font-size: 22px; margin: 5px 0; color: #722F37;">The Online Wine World Team</p>

        <div style="font-size: 14px; color: #888; margin-top: 40px; text-align: center; border-top: 1px solid #D4AF37; padding-top: 10px;">
            <p>For any questions about your order, please contact our Sommelier Service at wineryproject3@gmail.com</p>
            <p>© Online Wine World 2025</p>
        </div>
    </body>
    </html>
    """

    #plain_text provide a fallback option for email clients that cannot render HTML or for users who prefer plain text emails
    plain_text = f"""Cheers to Your Exquisite Selection - Online Wine World

Dear Wine Enthusiast,

Thank you for your exceptional taste and recent purchase from Online Wine World.
Your fine selections are being prepared with the utmost care and will be on their way to you shortly.

ORDER SUMMARY:
{formatted_items_list if formatted_items_list else "Your selected wines"}

Subtotal: ${order_summary['subtotal']:.2f}
Shipping: ${order_summary['shipping_cost']:.2f}
Tax: ${order_summary['tax']:.2f}
Total: ${order_summary['total']:.2f}

We recommend allowing your wines to rest for 24-48 hours after delivery before enjoying them at their optimal temperature.

"Wine is bottled poetry." — Robert Louis Stevenson

With appreciation for your distinguished palate,
The Online Wine World Team

For any questions about your order, please contact our Sommelier Service at wineryproject3@gmail.com
© Online Wine World 2025
"""

    # Set up the email message
    msg = EmailMessage()
    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype='html')

    msg['Subject'] = subject
    msg['From'] = OWN_EMAIL
    msg['To'] = user_email

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.send_message(msg)


def fetch_wine_details_by_purchase_id(purchase_id):
    """Fetch wine details from the database based on purchase_id."""
    query = """
    SELECT wine_name, price_at_purchase, quantity
    FROM purchase_items
    WHERE purchase_id = %s;
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (purchase_id,))
    result = cursor.fetchall()

    # Format result into a list of dictionaries
    wine_details = []
    for row in result:
        wine_details.append({
            'wine_name': row[0],
            'price_at_purchase': row[1],
            'quantity': row[2]
        })
    disconnection(conn,cursor)
    return wine_details
