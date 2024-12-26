#doctor.py
from src.model.user.user import User, Role

class Doctor(User):
    def __init__(
        self,
        id,
        name,
        email,
        password,
        role: Role = Role("doctor", ["read", "update", "create"]),
        gender: bool = None,
        born_date: str = None,
        born_place: str = None,
        domains: list = None,
    ):
        super().__init__(id, name, email, password, role,gender, born_date, born_place)
        self.domains = domains

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.to_dict(),
            "gender":self.gender,
            "born_date":self.born_date,
            "born_place":self.born_place,
            "domains": self.domains
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=Role.from_dict(data.get("role")),
            gender=data.get("gender"),
            born_date=data.get("born_date"),
            born_place=data.get("born_place"),
            domains=data.get("domains")
        )    