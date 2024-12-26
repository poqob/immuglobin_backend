from src.model.role import Role
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from configparser import ConfigParser
import pymongo

class Authenticate:
    def __init__(self, config_path="D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\src\\mongo.ini"):
        config = ConfigParser()
        config.read(config_path)
        self.client = pymongo.MongoClient(config["DATABASE"]["url"])
        self.db = self.client[config["DATABASE"]["client"]]
        self.users = self.db["users"]
        self.roles = self.db["roles"]

    def authenticate(self, email, password)->User:
        # Find the user by email
        user = self.users.find_one({"email": email, "password": password})
        if user is None:
            print("User not found")
            return None
        # Return the appropriate user object based on the role
        role = user.get("role")
        if role.get("role") == "doctor":
            return Doctor.from_dict(user)
        if role.get("role") == "patient":
            return Patience.from_dict(user)
        return None

    def close(self):
        self.client.close()

