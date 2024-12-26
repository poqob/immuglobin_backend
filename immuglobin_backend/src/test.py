# test.py
from src.model.role import Role
from src.model.user.user import User
from src.model.user.doctor import Doctor
from src.model.user.patience import Patience

from src.auth.authenticate import Authenticate
from src.auth.authorization import Authorize

def test_role():
    pass

def test_factory():
    role = Role("admin", ["create", "read", "update", "delete"])
    doctor = Doctor(1, "doctor", "email", "password",role,True,"12/12/1990","Bogota",["pediatrician"])
    another_doctor = Doctor.from_dict(doctor.to_dict())
    print(another_doctor.to_dict())

    patience = Patience(2, "patient", "email", "password",role,True,"12/12/1990","Bogota","yatan")
    another_patience = Patience.from_dict(patience.to_dict())
    print(another_patience.to_dict())

def test_authenticate():
    auth = Authenticate()
    user = auth.authenticate("doctor@gmail.com", "password")
    assert user is not None

def test_authorize():
    authen = Authenticate()
    auth = Authorize()
    user = authen.authenticate("doctor@gmail.com", "password")
    print( auth.authorize(user.email, "delete") )