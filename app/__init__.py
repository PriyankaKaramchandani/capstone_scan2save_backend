# from .services.firebase_services import create_app

# # Create the app instance
# app = create_app()

# # To start the Flask server when this file is executed directly
# if __name__ == '__main__':
#     app.run(debug=True)  


from flask import Flask
import os
from flask_cors import CORS
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from .routes.routes import bp as routes_bp

GOOGLE_APPLICATION_CREDENTIALS = {
  "type": "service_account",
  "project_id": "scan2save-faeee",
  "private_key_id": "75b7b087097f4ccc13ec30ac2b2b4863d51539b7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCmkRosPUDCxBRq\nTO2X+FKyXwJQH/veE0rc5rJF1cIW4N9acSZ2DZ6yHz59vAGzhrjq9NsAZIWxhuma\nhTsZ16LAT7EYz3wWfAf2TLFRSvvDjnqc1x+7PrxP7kkERqAZOsvVrGZVOf+TDWgy\niOhQJDMhivxCe3WpbmLXWKHG2oQ7CS4Lah3TAY0xl1dAfQmZythzwxaX9EYGyrup\nzzBse/3XspHNqRv4HDmWU/wTbHoCWaqqdXm3es8V2kL1WQvHsb+CCs7R/qcJ0AS4\nW2B6JVbID857D1XznQD8cg6+b8US8eWNoBjY9Teu5tKzZNUtzz93p9mTejNEav/9\nlaMHu/+7AgMBAAECggEAQD+SB+RsmXPGqCYaM1c+lrzdCIj9vvBUHRcDRrqoDekZ\nXips+nZQc0Zn9VnSkivyIfbmjqU3iH2Ql+CyJkqt5V4X4okNxSJ8c72rW77/k7Pe\niabU/4W4X2B7W6HeWTz7qOTB6Dfh5Bf0zCFQ8rCz5ElW+lHi1cLVb1kptalN/fLx\nRqP539pxcVsg8RRDQooTdZ+ETd9FPMsk3N4mb0Qpqyn4wVVmSRas27emj4sIoSFl\nvXIzmYW/JbDiYwRMx5mn8wX2JQLRZPVD61K/jBfZ2T/aAKv3DH08lsGcafIXZIEI\nhHulLPVTdJsPDUnPCzAxkrKEfKr8Hmw3Na3gBOXKmQKBgQDmR81V3Bdj7sIjYjN2\nXsMwzGr0+hqZu3W3RzEeMq/wVXU+LmMtT+lpp0gAcz7HKRuk+izaJ1XyAMjn09OW\n1GU+dQyzo2vXyUKz242PcYq6AEMP08eZsOSLxnZA61TskKuC9gCGM4QsvaBcIY1k\nzp14Ejf0zQhjq52nNDdfZI9adwKBgQC5K5f+90QTXlooIQhDRRpUPaOZK/yewPvI\nGWOdfOHd8GJfOX7UWjDT8Kl2/ZqiAXn8QxCUgddYSvkxNMvPoN70eKIZ0Kf9uiZv\n5VBikfErGAyNY/drzqmUnV4yMAEzZxRl6zhNI39G73ep2/4kEz/y7ujzIiO+gi9o\n/acpSg8R3QKBgHdLlS04oolro/kuo1hcCSRbkcEtW+BuQ7JZ2DE7svd/XgiDgW90\n6YeJWHybN1d3jVGvJNMy84w2Kd4nV4LYr0Zm3tik/XZBViPUxoYcHPD0t8kYPlv5\nTry2aIaDI3CWFbP3exgK0htXdR6lZxllDCCq14AjQ4hW3IpFO7ZYYwdLAoGASdnj\nIyNHGVp2Jq8V9o5m89Ypm3t5o29ge+v0WOlnw/aNpWDu/o6CDuVbEUQQGjDwj/XH\ndRNb6bDtNfzSlJqakXJTZGxds8o8bkBNESMXxpIu321RTsP7ynQBD48py3B/KC7q\nI4nWx1nWpf5Bm+25gZBbhCzHiMGvWvZfZw5MeFkCgYAt4FFc0MqoH4ZkPD/Awmg0\n9mnsBW1EQprmtl7lhyJqjMTIgTQKnep2PoDHovbm9l952TJh79xmmZ8uopuunHhq\nBXPUgD64Z4Y1i1NsYcDuTf7I4qcADSAD/g9sED+0r+uROi379eVueLLBRlz5c2wf\ngOdBpvqBVArvT+LtsdK1HA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@scan2save-faeee.iam.gserviceaccount.com",
  "client_id": "117144777886767348171",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40scan2save-faeee.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

SECRET_KEY = "my-very-secure-and-random-secret-key-12345"


# Load environment variables from the .env file
load_dotenv()

# Get the Firebase private key path from environment variables
firebase_private_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
secret_key = os.getenv('SECRET_KEY')

#Debug
print(f"Firebase private key path: {firebase_private_key_path}")
print(f"Secret key: {secret_key}")


def create_app(test_config=None):
    app = Flask(__name__)

    # Load configuration (e.g., from config.py or .env)
    app.config['SECRET_KEY'] = secret_key

    # Initialize CORS after the app is created
    CORS(app)

    if not firebase_private_key_path:
        raise ValueError("Firebase credentials path not set in environment variables.")

    # Path to your Firebase Admin SDK private key
    cred = credentials.Certificate(firebase_private_key_path)
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    app.firestore_db = firestore.client()

    # Register the blueprint
    app.register_blueprint(routes_bp)

    return app