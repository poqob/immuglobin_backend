from src.model.user.user import User
from src.model.referance.ref_data import RefValue,RefDataModel
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience
from src.model.role import Role
from  configparser import ConfigParser
import pymongo
import os
import json



def add_referances(referances):
    jsons_path = r'D:\Dosyalar\projeler\py\immuglobin_backend\immuglobin_backend\data\primitive_json'
    for filename in os.listdir(jsons_path):
            if filename.endswith('.json'):
                with open(os.path.join(jsons_path, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    referances.insert_one(data)    
        




def create_roles(roles):
    patient = Role("patient", ["read", "update"])
    doctor = Role("doctor", ["read", "update", "create", "delete"])
    roles.insert_one(patient.to_dict())
    roles.insert_one(doctor.to_dict())

def create_users(users, roles):
    patient_role = Role.from_dict(roles.find_one({"role": "patient"}))
    doctor_role = Role.from_dict(roles.find_one({"role": "doctor"}))  
    patient_user = Patience(11111111111, "irme", "irme@gmail.com", "password123", patient_role,False,"12/06/2003","Tokat","acil")
    doctor_user = Doctor(22222222222, "dağ", "dag@gmail.com", "password123", doctor_role,True,"04/02/2002","Bursa",["KBB"])
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
    referances = db["referances"]
    reports = db["reports"]
    # tests.drop()
    # users.drop()
    # roles.drop()
    referances.drop()
    reports.drop()
    # create_roles(roles)
    # create_users(users, roles)
    add_referances(referances)
    client.close()
