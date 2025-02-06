# from .services.firebase_services import create_app

# # Create the app instance
# app = create_app()

# # To start the Flask server when this file is executed directly
# if __name__ == '__main__':
#     app.run(debug=True)  


# from flask import Flask
# import os
# from flask_cors import CORS
# from dotenv import load_dotenv
# import firebase_admin
# from firebase_admin import credentials, firestore
# from .routes.routes import bp as routes_bp


# # Load environment variables from the .env file
# load_dotenv()

# # Get the Firebase private key path from environment variables
# firebase_private_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# secret_key = os.getenv('SECRET_KEY')

# #Debug
# print(f"Firebase private key path: {firebase_private_key_path}")
# print(f"Secret key: {secret_key}")


# def create_app(test_config=None):
#     app = Flask(__name__)

#     # Load configuration (e.g., from config.py or .env)
#     app.config['SECRET_KEY'] = secret_key

#     # Initialize CORS after the app is created
#     CORS(app)

#     if not firebase_private_key_path:
#         raise ValueError("Firebase credentials path not set in environment variables.")

#     # Path to your Firebase Admin SDK private key
#     cred = credentials.Certificate(firebase_private_key_path)
#     firebase_admin.initialize_app(cred)

#     # Initialize Firestore
#     app.firestore_db = firestore.client()

#     # Register the blueprint
#     app.register_blueprint(routes_bp)

#     return app

from flask import Flask
import os
from flask_cors import CORS
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from .routes.routes import bp as routes_bp

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

print(f"Secret key: {secret_key}")  # Keep this for debugging

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    CORS(app)

    # Initialize Firebase using Application Default Credentials
    try:
        cred = credentials.ApplicationDefault()  # Use ApplicationDefault()!
        firebase_admin.initialize_app(cred)
        app.firestore_db = firestore.client()
        print("Firebase initialized successfully!") # Important confirmation
    except Exception as e:
        print(f"Error initializing Firebase: {e}")  # Crucial error handling
        # Handle the error appropriately, e.g., exit the application
        return None # Or raise the exception, depending on your needs

    app.register_blueprint(routes_bp)
    return app