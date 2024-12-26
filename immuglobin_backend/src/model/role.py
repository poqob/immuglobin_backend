# role.py


class Role:
    def __init__(self, role: str, permissions: list):
        self.role = role
        self.permissions = permissions

    def __str__(self):
        return f"Role: {self.role}"

    def to_dict(self):
        return {
            "role": self.role,
            "permissions": self.permissions,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            role=data.get("role"),
            permissions=data.get("permissions"),
        )
