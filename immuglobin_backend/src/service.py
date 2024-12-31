from flask import Flask, jsonify, request
from configparser import ConfigParser
from pymongo import MongoClient
from src.methods.db_methods import get_all_users, get_user_by_email, add_user,delete_user,is_email_taken,password_limitations,change_password,change_email,is_id_taken,get_all_referances,add_report,delete_deport,get_all_reports,get_reports_by_user_idd,get_reports_by_user_namee,get_user_by_id,add_referance
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
    auth = Authenticate()
    user = auth.authenticate(data.get("email"), data.get("password"))
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404




@app.route('/authenticate', methods=['POST'])
def authenticate():
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
    if auth.authorize(data.get("email"),data.get("password") ,data.get("permissions")):
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
    id = data.get("id")
    
    if is_id_taken(id):
        return jsonify({"error": "ID already taken"}), 400

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    if is_email_taken(email):
        return jsonify({"error": "Email already taken"}), 400
    
    if not password_limitations(password):
        return jsonify({"error": "Password must be at least 8 characters long and contain at least one digit"}), 400

    result = add_user(data)
    
    return jsonify({"message": result}), 201

@app.route('/remove', methods=['POST'])
def remove_user():
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        result = delete_user(email, password)
        
        if result.get("error"):
            return jsonify(result), 400
        
        return jsonify(result), 201

@app.route('/change_password', methods=['POST'])
def change_pass():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    if not email or not old_password or not new_password:
        return jsonify({"error": "Email, old password and new password are required"}), 400
    
    if not password_limitations(new_password):
        return jsonify({"error": "Password must be at least 8 characters long and contain at least one digit"}), 400

    result = change_password(email, old_password, new_password)
    
    if result.get("error"):
        return jsonify(result), 400
    
    return jsonify(result), 201


@app.route('/change_email', methods=['POST'])
def change_mail():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get("old_email")
    new_email = data.get("new_email")
    password = data.get("password")
    
    if not email or not new_email or not password:
        return jsonify({"error": "Email, new email and password are required"}), 400
    
    result = change_email(email, new_email, password)
    
    if result.get("error"):
        return jsonify(result), 400
    
    return jsonify(result), 201

@app.route('/get_user_by_id', methods=['POST'])
def get_user_by_idd():
    data = request.json
    print(data)
    user = get_user_by_id(data.get('id'))
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/get_all_referances', methods=['GET'])
def get_all_referancess():
    referances = get_all_referances()
    if referances:
        return jsonify(referances)
    return jsonify({"error": "Referances not found"}), 404

@app.route('/get_all_reports', methods=['GET'])
def get_all_reportss():
    reports = get_all_reports()
    if reports:
        return jsonify(reports), 200
    return jsonify({"error": "Reports not found"}), 404


@app.route('/submit_report', methods=['POST'])
def add_reportt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    user_id = data.get("user_id")
    user_name = data.get("user_name")
    doctor_id = data.get("doctor_id")
    immun = data.get("immun")
    timestamp = data.get("timestamp")
    
    if not user_id or not doctor_id or not immun or not timestamp:
        return jsonify({"error": "User ID, doctor ID, immun, result and timestamp are required"}), 400
    
    result = add_report(user_id,user_name, doctor_id, immun, timestamp)

    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result), 201


@app.route('/remove_report', methods=['POST'])
def delete_deportt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    id = data.get("id")
    
    if not id:
        return jsonify({"error": "ID is required"}), 400
    
    result = delete_deport(id)

    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result), 201

@app.route('/get_reports_by_user_id', methods=['POST'])
def get_reports_by_user_id():
    data = request.json
    reports = get_reports_by_user_idd(data.get('user_id'))

    if reports:
        return jsonify(reports), 200
    return jsonify({"error": "Reports not found"}), 404


@app.route('/get_reports_by_user_name', methods=['POST'])
def get_reports_by_user_name():
    data = request.json
    reports = get_reports_by_user_namee(data.get('user_name'))
    if reports:
        return jsonify(reports), 200
    return jsonify({"error": "Reports not found"}), 404


@app.route('/submit_referance', methods=['POST'])
def add_referancee():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    result = add_referance(data)

    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
