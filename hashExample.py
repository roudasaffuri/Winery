import hashlib


def generate_hash(data):
    # Encode the data to bytes
    encoded_data = data.encode('utf-8')

    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(encoded_data)

    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()

    return hash_hex


# Example usage
data = "Hello, World!"
hash_code = generate_hash(data)
print(f"Hash code: {hash_code}")
