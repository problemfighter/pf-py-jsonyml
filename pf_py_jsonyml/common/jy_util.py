import inspect
import re
from typing import get_origin
from pf_py_jsonyml.jybase import JYBase


class JYDataType:
    name: str
    collection: str
    objectType: str
    dictKeyType: str
    collectionClass: str


class JYUtil:

    @staticmethod
    def try_to_get_field_type(data):
        try:
            return get_origin(data).__name__
        except:
            return None

    @staticmethod
    def get_collection_info(data_type):
        if data_type in ["list", "dict", "List", "Dict"]:
            return data_type
        return None

    @staticmethod
    def get_py_base_class_object(attr_name, class_object: JYBase):
        try:
            if hasattr(class_object, "get_globals") and attr_name in class_object.get_globals():
                class_object = class_object.get_globals()[attr_name]()
                if class_object:
                    return class_object
        except:
            return None
        return None

    @staticmethod
    def get_object_info(data_type, original_object):
        if data_type in ["list", "dict", "str", "int", "float", "bool"]:
            return "primitive"
        else:
            try:
                if hasattr(original_object, "get_globals") and data_type in original_object.get_globals():
                    class_name = original_object.get_globals()[data_type]
                    if class_name and issubclass(class_name, JYBase):
                        return "JYBase"
            except:
                pass
        return "Unknown"

    @staticmethod
    def parse_typing_data(system_name, data_type: JYDataType, class_object):
        pattern = re.compile("typing\\.([A-Za-z]+)\\[([\w\\.,\s]+)]")
        match = re.match(pattern, system_name)
        if not match or len(match.groups()) < 2:
            return None
        data_type.name = match.group(1).strip()
        data_type.collection = JYUtil.get_collection_info(data_type.name)
        object_type = match.group(2).strip()
        if data_type.collection == "Dict":
            key_value = object_type.split(",")
            data_type.dictKeyType = key_value[0].strip()
            object_type = key_value[1].strip()
        object_type = object_type.replace("__main__.", "")
        data_type.collectionClass = object_type
        data_type.objectType = JYUtil.get_object_info(object_type, class_object)
        return data_type

    @staticmethod
    def get_typing_value(value, data_type: JYDataType, class_object):
        system_name = str(value)
        if system_name.startswith("typing"):
            response = JYUtil.parse_typing_data(system_name, data_type, class_object)
            if response:
                return response

        data_type.name = JYUtil.try_to_get_field_type(value)
        data_type.collection = JYUtil.get_collection_info(data_type.name)
        data_type.objectType = JYUtil.get_object_info(data_type.name, class_object)
        return data_type

    @staticmethod
    def get_class_attrs(class_object) -> dict:
        name_and_data_type = {}
        for attrs in inspect.getmembers(class_object):
            if len(attrs) == 2 and attrs[0] == "__annotations__":
                for attr_name in attrs[1]:
                    data_type: JYDataType = JYDataType()
                    try:
                        data_type.name = attrs[1][attr_name].__name__
                        data_type.collection = JYUtil.get_collection_info(data_type.name)
                        data_type.objectType = JYUtil.get_object_info(data_type.name, class_object)
                    except:
                        data_type = JYUtil.get_typing_value(attrs[1][attr_name], data_type, class_object)
                    name_and_data_type[attr_name] = data_type
                break
        return name_and_data_type
