from flask import Blueprint, request, jsonify
from .utilities import validate_profile_completeness, generate_uuid, store_user_profile, store_medical_profile, generate_qr_code, retrieve_user_data
from .utilities import update_user_profile, update_user_medical_profile
from firebase_admin import firestore
import logging

bp = Blueprint('routes', __name__, url_prefix="/api")

# Route for new_user to create medical_profile
@bp.post("/new_user")
def create_a_new_profile():
    try:
        data = request.get_json()

        valid_roles = ['new_user', 'returning_user', 'medical_professional']
        required_steps = ['first_name', 'last_name', 'date_of_birth']

        is_valid, message = validate_profile_completeness(data, valid_roles, required_steps)

        if not is_valid:
            return jsonify({"error": message}), 400

        # Generate a unique UUID
        user_id = generate_uuid()
        profile_id = generate_uuid()

        # Generate a unique URL using the UUID
        unique_url = f"https://scan2save.com/user/{user_id}"

        # Generate and encode QR code
        qr_code_base64 = generate_qr_code(unique_url)

        # Store the user profile data in Firestore
        store_user_profile(user_id, data, qr_code_base64)

        # Store the medical profile data
        store_medical_profile(profile_id, user_id, data)

        logging.info(f"New user created successfully with user_id: {user_id}")

        return jsonify({
            "message": "New user created successfully", 
            "user_id": user_id, 
            "unique_url": unique_url, 
            "qr_code_base64": qr_code_base64
            }), 201
    except Exception as e:
        logging.error(f"Error creating new user profile: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Route to get user data and associated medical data:used by new and existing users
@bp.get("/user/<user_id>")
def get_user_profile(user_id):
    try:
        user_data, medical_profiles = retrieve_user_data(user_id)
        if user_data is None:
            return jsonify({"error": "User not found"}), 404
        
        logging.debug(f"User data retrieved: {user_data}")

        response = {
            "user_data": user_data,
            "qr_code_base64": user_data.get('qr_code_base64'),
            "qr_code_type": user_data.get('qr_code_type') 
        }

        if medical_profiles is not None:
            response["medical_profiles"] = medical_profiles

        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error retrieving user profile: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Route to update user or medical profile for existing users: Didnt complete this feature-future goal
@bp.patch("/user/<user_id>/update")
def update_user_or_medical_profile(user_id):
    try:
        data = request.get_json()
        user_updates = data.get("user_updates", {})
        medical_updates = data.get("medical_updates", {})

        # Update user profile if updates are provided
        user_success = True
        user_error = None
        if user_updates:
            user_success, user_error = update_user_profile(user_id, user_updates)
            if not user_success:
                return jsonify({"error": f"User update failed: {user_error}"}), 404

        # Update medical profile if updates are provided
        medical_success = True
        medical_error = None
        if medical_updates:
            medical_success, medical_error = update_user_medical_profile(user_id, medical_updates)
            if not medical_success:
                return jsonify({"error": f"Medical profile update failed: {medical_error}"}), 404

        # If both updates are successful
        if user_success and medical_success:
            return jsonify({"message": "User and medical profile updated successfully"}), 200
        else:
            return jsonify({"error": "Update failed"}), 400

    except Exception as e:
        logging.error(f"Error updating user or medical profile: {e}")
        return jsonify({"error": "Internal server error"}), 500

