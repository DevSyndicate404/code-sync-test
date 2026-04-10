from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_valid_email(email):
    # Basic regular expression for email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@app.route('/validate', methods=['POST'])
def validate_credentials():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email', '')
    password = data.get('password', '')

    errors = []

    # Validate Email
    if not email:
        errors.append("Email is required.")
    elif not is_valid_email(email):
        errors.append("Invalid email format.")

    # Validate Password (example: min 8 characters)
    if not password:
        errors.append("Password is required.")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    return jsonify({"status": "success", "message": "Validation passed"}), 200

if __name__ == '__main__':
    app.run(debug=True)
