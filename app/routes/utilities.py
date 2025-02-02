from firebase_admin import firestore
from uuid import uuid4
import logging
import qrcode
import base64
from io import BytesIO
from flask import request

# Validate profile being complete
def validate_profile_completeness(data, valid_roles, required_steps):
    required_fields = ['first_name', 'last_name', 'date_of_birth', 'role']

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing or empty field: {field}"

        role = data.get('role')
        if role not in valid_roles:
            return False, f"Invalid role: {role}. Valid roles are: {', '.join(valid_roles)}"

        #  # Check if all required steps are completed
        # for step in required_steps:
        #     if step not in data.get('completed_steps', []):
        #         return False, f"Missing required step: {step}"

        # return True, "Profile is complete"
        # completed_steps = data.get('completed_steps')
        # if not completed_steps or not all(step in completed_steps for step in required_steps):
        #     return False, f"Incomplete steps. The following steps are required: {', '.join(required_steps)}"
    
        # Check for duplicates in Firestore
        db = firestore.client()
        users_ref = db.collection('users')
        query = users_ref.where('first_name', '==', data['first_name']) \
                        .where('last_name', '==', data['last_name']) \
                        .where('date_of_birth', '==', data['date_of_birth'])
        duplicates = query.stream()

        if any(duplicates):
            return False, "A profile with the same first name, last name, and date of birth already exists."

    return True, None

# Generate a unique UUID
def generate_uuid():
    return str(uuid4())


# Store the user profile data in Firestore
def store_user_profile(user_id, data, qr_code_base64):
    db = firestore.client()
    user_data = {
        'user_id': user_id,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'date_of_birth': data['date_of_birth'],
        'gender': data.get('gender', ''),
        'phoneNumber': data.get('phoneNumber', ''),
        'role': data['role'],
        'emergency_contact': {
            'first_name': data.get('emergency_contact', {}).get('first_name', ''),
            'last_name': data.get('emergency_contact', {}).get('last_name', ''),
            'phone_number': data.get('emergency_contact', {}).get('phone_number', ''),
        },
        # 'completed_steps': data['completed_steps'],
        'qr_code_base64': qr_code_base64
    }
    db.collection('users').document(user_id).set(user_data)


# Store the medical profile data
def store_medical_profile(profile_id, user_id, data):
    logging.info(f"Storing medical profile for user_id: {user_id} with profile_id: {profile_id}")
    db = firestore.client()
    medical_profile_data = {
        'profile_id': profile_id,
        'user_id': user_id,
        'blood_group': data.get('blood_group', ''), 
        'allergies': data.get('allergies', []), 
        'past_surgeries': data.get('past_surgeries', []), 
        'medications': data.get('medications', []),
        'pregnant': data.get('pregnant', ''),
        'preferences': {
            'do_not_resuscitate': data.get('preferences', {}).get('do_not_resuscitate', False),
            'organ_donor_status': data.get('preferences', {}).get('organ_donor_status', False),
        },
        'QRCode': {
            'qr_code_url': f"https://scan2save.com/user/{user_id}/qr",
            'qr_code_type': data.get('QRCode', {}).get('qr_code_type', 'emergency'),
        },
        'preferred_hospital': data.get('preferred_hospital', ''),
        'special_instructions': data.get('special_instructions', '')
    }
    db.collection('medical_profiles').document(profile_id).set(medical_profile_data)
    logging.info(f"Medical profile stored successfully for profile_id: {profile_id}")


# Generate and encode QR code
def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

# Retrieve user_data or user_data + medical_profile based on query parameters: partial
def retrieve_user_data(user_id):
    db = firestore.client()

    # Retrieve user_data
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return None, "User not found"
    user_data = user_doc.to_dict()

    # Check for query parameters to determine if partial or full data is needed
    partial = request.args.get('partial', 'false').lower() == 'true'

    if partial:
        # Return only user data
        return user_data, None
    else:
        # Retrieve associated medical profile data
        medical_profile_ref = db.collection('medical_profiles').where('user_id', '==', user_id)
        medical_profiles_docs = medical_profile_ref.stream()
        medical_profiles = [doc.to_dict() for doc in medical_profiles_docs]
        return user_data, medical_profiles
    

# Helper function to update user profile
def update_user_profile(user_id, updated_fields):
    if not updated_fields:
        logging.info("No user updates to apply.")
        return True, None  # No updates to apply

    try:
        # Retrieve the user document from Firestore
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            logging.warning(f"User document with ID {user_id} does not exist.")
            return False, "User not found"

        # Update the user profile fields
        user_ref.update(updated_fields)
        logging.info(f"User profile updated for user ID {user_id}.")
        return True, None
    except Exception as e:
        logging.error(f"Error updating user profile for user ID {user_id}: {e}", exc_info=True)
        return False, str(e)

def update_user_medical_profile(user_id, updated_fields):
    if not updated_fields:
        logging.info("No medical updates to apply.")
        return True, None  # No updates to apply

    try:
        # Retrieve the medical profile document from Firestore
        db = firestore.client()
        medical_profile_ref = db.collection('medical_profiles').where('user_id', '==', user_id)
        medical_profiles_docs = medical_profile_ref.stream()

        if not medical_profiles_docs:
            logging.warning(f"No medical profile documents found for user ID {user_id}.")
            return False, "Medical profile not found"

        # Update the medical profile fields
        for doc in medical_profiles_docs:
            doc.reference.update(updated_fields)
        logging.info(f"Medical profile updated for user ID {user_id}.")
        return True, None
    except Exception as e:
        logging.error(f"Error updating medical profile for user ID {user_id}: {e}", exc_info=True)
        return False, str(e)
