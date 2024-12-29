from typing import  Optional
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

