from typing import List, Dict
from pf_py_jsonyml.jybase import JYBase
from pf_py_jsonyml.object_dict import ObjectDict


class Degree(JYBase):
    name: str

    def __init__(self, name):
        self.name = name


class Address(JYBase):
    country: str

    def __init__(self, country: str = None):
        self.country = country


class Profile(JYBase):
    gender: str
    mobile: str
    address: Address

    def __init__(self, gender: str, mobile: str):
        self.gender = gender
        self.mobile = mobile


class Person(JYBase):
    id: int
    firstName: str
    lastName: str
    salary: float
    isMarried: bool
    profile: Profile
    degrees: List[Degree]
    simpleList: list
    simpleDict: dict
    otherAddress: Dict[str, Address]


person1 = Person()
person1.id = 1
person1.firstName = "Touhid"
person1.lastName = "Mia"
person1.salary = 10000
person1.isMarried = True
person1.profile = Profile(gender="Male", mobile="1234")
person1.degrees = [Degree("Primary"), Degree("Secondary"), Degree("Bsc")]
person1.simpleList = ["A", "B", "C", "D"]
person1.simpleDict = {"a": "A", "b": "B"}
person1.otherAddress = {"home": Address("Bangladesh"), "office": Address("Canada")}


object_dict = ObjectDict()
print(object_dict.get_dict(person1))
