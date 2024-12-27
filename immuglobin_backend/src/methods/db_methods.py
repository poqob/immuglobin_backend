from configparser import ConfigParser
from pymongo import MongoClient

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
    result = users_collection.insert_one(user_data)
    return {"inserted_id": str(result.inserted_id)}

# Function to check if email already exists
def is_email_taken(email):
    return users_collection.find_one({"email": email}) is not None

def password_limitations(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True