from src.model.user.user import User
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from src.model.role import Role
from  configparser import ConfigParser
import pymongo



def create_tests(tests):
    pass





def create_roles(roles):
    admin = Role("admin", ["create", "read", "update", "delete"])
    patient = Role("patient", ["read", "update"])
    doctor = Role("doctor", ["read", "update", "create", "delete"])
    roles.insert_one(admin.to_dict())
    roles.insert_one(patient.to_dict())
    roles.insert_one(doctor.to_dict())

def create_users(users, roles):
    patient_role = Role.from_dict(roles.find_one({"role": "patient"}))
    doctor_role = Role.from_dict(roles.find_one({"role": "doctor"}))  
    patient_user = Patience(3, "patient", "patient@gmail.com", "password", patient_role,True,"12/12/1990","Bogota","yatan")
    doctor_user = Doctor(4, "doctor", "doctor@gmail.com", "password", doctor_role,True,"12/12/1990","Bogota")
    users.insert_one(patient_user.to_dict())
    users.insert_one(doctor_user.to_dict())



def build():
    config = ConfigParser()
    config.read("D:\\Dosyalar\\projeler\\py\\immuglobin_backend\\immuglobin_backend\\mongo.ini")
    client = pymongo.MongoClient(config["DATABASE"]["url"])
    db = client["local"]
    users = db["users"]
    roles = db["roles"]
    tests=db["tests"]
    tests.drop()
    users.drop()
    roles.drop()
    create_roles(roles)
    create_users(users, roles)
    create_tests(tests)
    client.close()
