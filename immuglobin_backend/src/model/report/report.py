import hashlib

class Report:
    def __init__(self,user_id,doctor_id,immun,result,timestamp):
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.immun = immun
        self.result = result
        self.timestamp = timestamp
        self.id=self._generate_unique_id()
        
    
    def __str__(self):
        return f"Report: {self.user_id} {self.doctor_id} {self.immun} {self.result} {self.date}"
    
    def _generate_unique_id(self):
        unique_string = f"{self.timestamp}{self.result}{self.user_id}{self.doctor_id}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "doctor_id": self.doctor_id,
            "immun": self.immun,
            "result": self.result,
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            doctor_id=data.get("doctor_id"),
            immun=data.get("immun"),
            result=data.get("result"),
            date=data.get("timestamp"),
        )
    
# if __name__=='__main__':
#     a = Report(1,2,"immun","result","12/12/2020")
#     print(a.generate_unique_id())
#     b=Report(1,2,"immun","result","12/12/2020")
#     print(b.generate_unique_id())