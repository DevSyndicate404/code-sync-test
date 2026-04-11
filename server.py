from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta



# Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelthours=1)
jwt = JWTManager(app)

# In-memory database for demonstration
# structure: { username: { "pw_hash": str, "created_at": str } }
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    if len(password) < 4:
        return jsonify({"msg": "Password must be at least 4 characters"}), 400
    
    if username in users:
        return jsonify({"msg": "User already exists"}), 400

    users[username] = {
        "pw_hash": generate_password_hash(password),
        "created_at": datetime.utcnow().isoformat()
    }
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if not user or not check_password_hash(user['pw_hash'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user_record = users.get(current_user, {})
    
    return jsonify({
        "logged_in_as": current_user,
        "account_created": user_record.get('created_at'),
        "server_status": "Healthy",
        "message": "Access granted to protected resource"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)