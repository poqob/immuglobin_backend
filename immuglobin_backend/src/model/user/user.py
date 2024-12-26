# user.py
from abc import ABC, abstractmethod
from src.model.role import Role


class User(ABC):
    def __init__(
        self, id, name, email, password, role: Role, gender:bool, born_date, born_place
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.gender = gender
        self.born_date = born_date
        self.born_place = born_place

    @abstractmethod
    def to_dict(self):
        return {"type": self.__class__.__name__}
