import os
from os.path import exists
from typing import Union
import yaml
from pf_py_jsonyml.jybase import JYBase
from pf_py_jsonyml.object_dict import ObjectDict


class YamlConverter:
    object_dict = ObjectDict()

    def dict_to_yaml(self, data: dict) -> Union[str, None]:
        try:
            return yaml.dump(data, sort_keys=False)
        except Exception as e:
            return None

    def yaml_to_dict(self, yaml_content: str, default=None) -> Union[dict, None]:
        try:
            return yaml.full_load(yaml_content)
        except Exception as e:
            return default

    def object_to_yaml(self, data_object: JYBase) -> Union[str, None]:
        dict_data = self.object_dict.get_dict(data_object)
        if dict_data:
            return self.dict_to_yaml(dict_data)
        return None

    def yaml_to_object(self, yaml_content: str, data_object: JYBase, default=None) -> Union[JYBase, None]:
        dict_data = self.yaml_to_dict(yaml_content)
        if dict_data:
            return self.object_dict.get_object(dict_data, data_object)
        return default

    def write_yaml_object_to_file(self, file_path_with_name: str, data_object: JYBase) -> bool:
        if not file_path_with_name or not data_object:
            return False

        try:
            if exists(file_path_with_name):
                os.remove(file_path_with_name)

            yaml_content = self.object_to_yaml(data_object)
            if not yaml_content:
                return False

            stream = open(file_path_with_name, 'w', encoding="utf-8")
            stream.write(yaml_content)
            stream.close()
            return True
        except Exception as e:
            return False

    def read_yaml_object_from_file(self, file_path_with_name: str, data_object: JYBase, default=None) -> Union[JYBase, None]:
        if not exists(file_path_with_name):
            return default

        try:
            stream = open(file_path_with_name, 'r', encoding="utf-8")
            yaml_content = stream.read()
            return self.yaml_to_object(yaml_content, data_object, default=default)
        except Exception as e:
            return default
