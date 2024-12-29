from typing import List, Optional
import json

class RefValue:
    def __init__(self, subj: int, gms: float, min: float, max: float, 
                 min_age: Optional[int] = None, max_age: Optional[int] = None):
        self.subj = subj
        self.gms = gms
        self.min = min
        self.max = max
        self.min_age = min_age
        self.max_age = max_age

    def __repr__(self):
        return f"Value(subj={self.subj}, gms={self.gms}, min={self.min}, max={self.max}, " \
               f"min_age={self.min_age}, max_age={self.max_age})"


class RefDataModel:
    def __init__(self, imm: str, ref: str, values: List[RefValue]):
        self.imm = imm
        self.ref = ref
        self.values = values

    def __repr__(self):
        return f"DataModel(imm={self.imm}, ref={self.ref}, values={self.values})"


    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        values = [RefValue(**value) for value in data['values']]
        return cls(imm=data['imm'], ref=data['ref'], values=values)


path = './primitive_json/ig_tjp.json'

with open(path, 'r') as file:
    json_str = file.read()
    # print(json_str)
data_from_json = RefDataModel.from_json(json_str)

for value in data_from_json.values:
    print(value)