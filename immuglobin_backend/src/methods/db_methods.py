from configparser import ConfigParser
from pymongo import MongoClient
from src.model.user.user import User
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience


config_path="D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\mongo.ini"
config = ConfigParser()
config.read(config_path)

client = MongoClient(config["DATABASE"]["url"])
db = client["local"]
users_collection = db["users"]
roles_collection = db["roles"]


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

def password_limitations(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True