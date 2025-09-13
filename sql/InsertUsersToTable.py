#python code to insert users in table users PGadmin:
from backend.server.db_connection import create_connection
from faker import Faker
import random
import base64
from datetime import datetime
from cryptography.fernet import Fernet

# ---------------------
# Setup
# ---------------------

# Initialize Faker
fake = Faker()

# Generate a Fernet encryption key (should be stored securely in real apps)
# You can also use a hardcoded key or load from a .env or secrets file
fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)

# Function to encrypt and base64-encode password
def encrypt_and_encode_password(password):
    encrypted = cipher.encrypt(password.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# ---------------------
# Connect to DB
# ---------------------
conn = create_connection()
cur = conn.cursor()



# Get current year to calculate birth year
current_year = datetime.now().year

# ---------------------
# Insert 500 users
# ---------------------
for _ in range(500):
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = fake.unique.email()
    password = encrypt_and_encode_password("password123")
    birth_year = random.randint(current_year - 70, current_year - 18)  # Age 18–70
    gender = random.choice(["Male", "Female"])
    is_admin = False

    cur.execute("""
        INSERT INTO users (firstname, lastname, email, password, birth_year, gender, is_admin)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (firstname, lastname, email, password, birth_year, gender, is_admin))

# Commit and disconnect
conn.commit()
cur.close()
conn

print("✅ Successfully inserted 500 users with encrypted Base64 passwords.")