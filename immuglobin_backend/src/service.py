from flask import Flask, jsonify, request
from configparser import ConfigParser
from pymongo import MongoClient
from src.methods.db_methods import get_all_users, get_user_by_email, add_user,is_email_taken,password_limitations
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from src.auth.authenticate import Authenticate
from src.auth.authorization import Authorize

app = Flask(__name__)
config_path="D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\mongo.ini"
config = ConfigParser()
config.read(config_path)

client = MongoClient(config["DATABASE"]["url"])
db = client["local"]
users_collection = db["users"]
roles_collection = db["roles"]

@app.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users)

@app.route('/users/<email>', methods=['GET'])
def get_user(email):
    user = get_user_by_email(email)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    if not user_data:
        return jsonify({"error": "Invalid input"}), 400
    
    result = add_user(user_data)
    return jsonify(result), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    print(data)
    auth = Authenticate()
    user = auth.authenticate(data.get("email"), data.get("password"))
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404


@app.route('/authorize', methods=['POST'])
def authorize():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    auth = Authorize()
    if auth.authorize(data.get("email"), data.get("permission")):
        return jsonify({"message": "Authorized"})
    return jsonify({"error": "Unauthorized"}), 401


# no any firm requirements for registration
# User registration route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    if is_email_taken(email):
        return jsonify({"error": "Email already taken"}), 400
    
    if not password_limitations(password):
        return jsonify({"error": "Password must be at least 8 characters long and contain at least one digit"}), 400
    
    result = add_user(data)
    
    return jsonify({"message": "User registered successfully", "inserted_id": str(result["inserted_id"])}), 201


if __name__ == '__main__':
    app.run(debug=True)
