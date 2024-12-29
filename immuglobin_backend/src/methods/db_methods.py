from configparser import ConfigParser
from pymongo import MongoClient
from src.model.user.user import User
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from src.model.referance.ref_data import RefDataModel,RefValue
from src.model.report.report import Report


config_path="D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\mongo.ini"
config = ConfigParser()
config.read(config_path)

client = MongoClient(config["DATABASE"]["url"])
db = client["local"]
users_collection = db["users"]
roles_collection = db["roles"]
referance_collection = db["referances"]
report_collection = db["reports"]

def get_all_users():
    return list(users_collection.find({}, {"_id": 0}))

def get_user_by_email(email):
    return users_collection.find_one({"email": email}, {"_id": 0})

def add_user(user_data):
    #parse user data
    user = None
    if user_data["role"]["role"] == "doctor":
        user = Doctor.from_dict(user_data)
    elif user_data["role"]["role"] == "patience" or user_data["role"]["role"] == "patient":
        user = Patience.from_dict(user_data)
    else:
        return {"error": "Invalid user role"}

    result = users_collection.insert_one(user.to_dict())
    return {"inserted_id": str(result.inserted_id)}


def delete_user(email, password):
    try:
        result = users_collection.delete_one({"email": email, "password": password})
        if result.deleted_count == 0:
            return {"error": "User not found or incorrect password"}
        return {"message": "User deleted"}
    except Exception as e:
        return {"error": str(e)}



def change_password(email, old_password, new_password):
    result = users_collection.update_one({"email":email, "password":old_password}, {"$set": {"password":new_password}})
    if result.modified_count == 0:
        return {"error": "User not found or incorrect password"}
    return {"message": "Password changed"}


def change_email(email, new_email, password):
    result = users_collection.update_one({"email":email,"password":password}, {"$set": {"email":new_email}})
    if result.modified_count == 0:
            return {"error": "User not found. Incorrect password or email"}
    return {"message": "E-Mail changed"}

# Function to check if email already exists
def is_email_taken(email):
    return users_collection.find_one({"email": email}) is not None

def is_id_taken(id):
    return users_collection.find_one({"id": id}) is not None

def password_limitations(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

def get_all_referances():
    res = list(referance_collection.find({}, {"_id": 0}))
    return res

def get_all_reports():
    res = list(report_collection.find({}, {"_id": 0}))
    return res

def get_reports(user_id):
    res = list(report_collection.find({"user_id": user_id}, {"_id": 0}))
    return res


def add_report(user_id, doctor_id, immun, result, timestamp):
    report = Report(user_id, doctor_id, immun, result, timestamp)
    result = report_collection.insert_one(report.to_dict())
    if result.inserted_id is None:
        return {"error": "Report not inserted"}
    return {"inserted_id": str(result.inserted_id)}

def delete_deport(id):
    result = report_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"error": "Report not found"}
    return {"message": "Report deleted"}

