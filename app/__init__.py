# from .services.firebase_services import create_app

# # Create the app instance
# app = create_app()

# # To start the Flask server when this file is executed directly
# if __name__ == '__main__':
#     app.run(debug=True)  


from flask import Flask
import os
from flask_cors import CORS
# from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from .routes.routes import bp as routes_bp

GOOGLE_APPLICATION_CREDENTIAL = {
  "type": "service_account",
  "project_id": "scan2save-faeee",
  "private_key_id": "c99a12c00554c1c51d72ee4968653fc35859d644",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4xQara9trjiPQ\nw01PaiOSe8e5BUrKQyYyUap2JoM+bJYA9PofKihmvh44s+2o35AFTGCMtq/3Ftza\n6lU6R6s/Y3l7EgIbbVMC70UUhtCBRF2xS/NHPh4Gwl3YTlzhmHOjgAVbJBJJx4E7\na4o+btGRdJyx0EleCk/NLbxKNC8EAmyfPKQMnIG3y7tjQU8jc4aUrDMSeEJxznob\n4OKR63ZSE61VAhDZJ0TzHt0B+Q8cZsI2zJHB/dPO+5UgUYJms+zX/jq7WrBJ7frD\nelM+CE2kk2MTubU3ccN7fPDKQ6QnE3LlCcggzDtJaBCwJHWzOcS+veUEjp5RRDLE\nPQG96iovAgMBAAECggEAVITX7LEdQUFXU8cKxcF0/Sw+630mvYfi4JCny30JexQb\nt9tX0MqtiXX9CA4SMDX3wNyzq5pjusDMDR21F8Ax7wCXULsnmJk1KDoAHQggN4lo\n3FG0OooJHSlq2SfbZ9yfRRKqIItLDFHE5UPnjHCPz5wKk3IGJYzM/TunDkB5ozib\nhkPbqj3LOhFqW2WBAwNs6NG/rDjfG0YVAR3nlDzM9RSjkIHtgv+Ljm/liEt9RrmJ\nL618Uj5y9DPihIIA5kYySsQ6My8d1BpitmH/qoIC4EUQ/If8MNCG7ahhUsVPQIHJ\njyOiE3qNnk79F59RrqZ+LQHeF962TMMIkAweB719uQKBgQDi0RnIyOMaAS+kV1am\nLcfuW0fbS8FVN32fX5q5RtJ5GMQNsPoWLbQTAtdKtQPFVoSSMwpK5SNQDyRVFiVs\nHMnnsN1cSSb3kfKWL3FLljln7dSVFe3xnBD/51ZPZpaKvehnGEgJjVVkU64qitcS\nD2Zg6r/66NTHHNmYd7QGzvNcCQKBgQDQivlvvTprYdd0+lXIsS4d1sOie9/ZZMfq\n65eKZgYGkBIwhRWRzk2jWem7UGDGDwIsPzjPBs9ThposkhlJysT3hRnDryiBP7Bt\nNZh877EZklEHHX+4/n5Z4mMBKHVMSlprC5WOIXlmk9vdk07seN3UtyQUqaLgaRbV\nCopn17PSdwKBgFt+6DzTtLD3y4Uq6jxM+XrQfbMb4xiCMv3IbjzRMfRBpkyzmJ67\nvwlwOvLbBHNljEMBreQ6fL097nUYYu4yysvYz+L7a2mxCT/GUZihN/URvpCJcRvm\nzgC9DFcpVg8PvqFf7SdVSR4Yl4h3y3xwk+cCq4EGzVao76oOl6OrdgYpAoGAcfpz\nCDJJOqV4J9QmjJDiHqbht+2yU9P0PB5VbewDARU/C8vBFTbHUi9zQtBUhAtx6ZMI\nToZvTDx2CUQ0lBNCAfJ6OWyDW9jeaWHwnOA4UDybEqN5yjc2AZRs/hYJvg+pSXZE\nYDFFc93+PiUj7rTEsV0DWFO61KI7O2cObGEFRFMCgYBYVRY1C0DSEYbzL6o6XSK/\nk1p7w3FZ4+pGpuFqRka1AliodVjmVQVbXhaDRKTdApkrXZbShdcX7o7etM1nWbDr\nxDHpDBO/MWGiT25+ENp2+Ssx013sVSRE9aWVVzyT2kzP5QLXS1Zw9mK9iA6gaPCu\n4qD0w7SkEUHDF0duxKzC1A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@scan2save-faeee.iam.gserviceaccount.com",
  "client_id": "117144777886767348171",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40scan2save-faeee.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Load environment variables from the .env file
# load_dotenv()

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