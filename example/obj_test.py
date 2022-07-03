from typing import List, Dict
from pf_py_jsonyml.jybase import JYBase
from pf_py_jsonyml.object_dict import ObjectDict
from pf_py_jsonyml.yaml.yaml_converter import YamlConverter


class Degree(JYBase):
    name: str

    def __init__(self, name=None):
        self.name = name

    def get_globals(self):
        return globals()


class Address(JYBase):
    country: str

    def __init__(self, country: str = None):
        self.country = country

    def get_globals(self):
        return globals()


class Profile(JYBase):
    gender: str
    mobile: str
    address: Address

    def __init__(self, gender: str = None, mobile: str = None):
        self.gender = gender
        self.mobile = mobile

    def get_globals(self):
        return globals()


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

    def get_globals(self):
        return globals()


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
print(object_dict.get_dict(person1, is_ignore_none=True))

dict_object = {
    'id': 1,
    'firstName': 'Touhid',
    'lastName': 'Mia',
    'salary': 10000,
    'isMarried': True,
    'profile': {
        'gender': 'Male', 'mobile': '1234', 'address': None
    },
    'degrees': [
        {'name': 'Primary'},
        {'name': 'Secondary'},
        {'name': 'Bsc'}
    ],
    'simpleList': ['A', 'B', 'C', 'D'],
    'simpleDict': {'a': 'A', 'b': 'B'},
    'otherAddress': {
        'home': {'country': 'Bangladesh'},
        'office': {'country': 'Canada'}
    }
}

person_object: Person = object_dict.get_object(dict_object, Person())
print(person_object)


# YAML Conversion testing
yaml_converter = YamlConverter()
response = yaml_converter.object_to_yaml(person_object)
print(response)

yaml_content = """
id: 1
firstName: Touhid
lastName: Mia
salary: 10000
isMarried: true
profile:
  gender: Male
  mobile: '1234'
  address: null
degrees:
- name: Primary
- name: Secondary
- name: Bsc
simpleList:
- A
- B
- C
- D
simpleDict:
  a: A
  b: B
otherAddress:
  home:
    country: Bangladesh
  office:
    country: Canada
"""

person_yaml = Person()
response = yaml_converter.yaml_to_object(yaml_content, person_yaml)
print(response)
