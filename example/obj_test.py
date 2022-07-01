from pf_py_jsonyml.jybase import JYBase
from pf_py_jsonyml.object_dict import ObjectDict


class Address(JYBase):
    country: str


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


person1 = Person()
person1.id = 1
person1.firstName = "Touhid"
person1.lastName = "Mia"
person1.salary = 10000
person1.isMarried = True
person1.profile = Profile(gender="Male", mobile="1234")


object_dict = ObjectDict()
print(object_dict.get_dict(person1))
