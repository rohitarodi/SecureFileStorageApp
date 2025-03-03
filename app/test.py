import os
import base64

key = os.urandom(32)  # Generate 32 bytes random key
print(base64.b64encode(key).decode())  # Store this in your .env file
