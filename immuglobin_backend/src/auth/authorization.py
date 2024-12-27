from src.model.role import Role
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from configparser import ConfigParser
import pymongo

class Authorize:
    def __init__(self, config_path="D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\mongo.ini"):
        config = ConfigParser()
        config.read(config_path)
        self.client = pymongo.MongoClient(config["DATABASE"]["url"])
        self.db = self.client[config["DATABASE"]["client"]]
        self.users = self.db["users"]
        self.roles = self.db["roles"]

    def authorize(self, email, action)->bool:
         # Find the user by email
        user = self.users.find_one({"email": email})
        if user is None:
            print("User not found")
            return False
        # Return the appropriate user object based on the role
        role = user.get("role")
        if role is not None:
            return action in role.get("permissions")
        return False

    def close(self):
        self.client.close()