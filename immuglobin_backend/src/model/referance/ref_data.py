from typing import List
import json
from src.model.referance.ref_value import RefValue  


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

# if __name__=='__main__':
#     path = '../../../data/primitive_json/ig_tjp.json'

#     with open(path, 'r') as file:
#         json_str = file.read()
#         # print(json_str)
#     data_from_json = RefDataModel.from_json(json_str)

#     for value in data_from_json.values:
#         print(value)