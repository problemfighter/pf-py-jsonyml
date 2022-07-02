from pf_py_jsonyml.common.jy_util import JYUtil, JYDataType
from pf_py_jsonyml.jybase import JYBase
from typing import List, Dict


class ObjectDict:

    def _process_value(self, data):
        if not data:
            return data
        if isinstance(data, JYBase):
            data = self.get_dict(data)
        elif isinstance(data, List):
            data = self._handle_internal_list(data)
        elif isinstance(data, Dict):
            data = self._handle_internal_dict(data)
        return data

    def _handle_internal_list(self, list_data):
        response = []
        for item in list_data:
            item = self._process_value(item)
            response.append(item)
        return response

    def _handle_internal_dict(self, dict_data):
        response = {}
        for item_name in dict_data:
            response[item_name] = self._process_value(dict_data[item_name])
        return response

    def get_dict(self, data_object: JYBase):
        response_dict = {}
        data_and_type_map = JYUtil.get_class_attrs(data_object)
        for field_name in data_and_type_map:
            data = None
            if hasattr(data_object, field_name):
                data = getattr(data_object, field_name)
                data = self._process_value(data)
            response_dict[field_name] = data
        return response_dict

    def _set_value_to_object(self, data_name: str, data: dict, data_and_type_map: dict, data_object: JYBase):
        if data_name in data_and_type_map:
            jy_data_type: JYDataType = data_and_type_map[data_name]
            value = None
            if jy_data_type.name == "Dict" and jy_data_type.objectType == "JYBase":
                pass
            elif jy_data_type.name == "List" and jy_data_type.objectType == "JYBase":
                pass
            elif jy_data_type.objectType == "JYBase":
                jy_base_object = JYUtil.get_py_base_class_object(jy_data_type.name, data_object)
                if jy_base_object:
                    value = self.get_object(data[data_name], jy_base_object)
            else:
                value = data[data_name]
            setattr(data_object, data_name, value)
        return data_object

    def get_object(self, data: dict, data_object: JYBase):
        if not data or not data_object:
            return None
        data_and_type_map = JYUtil.get_class_attrs(data_object)
        for item_name in data:
            data_object = self._set_value_to_object(item_name, data=data, data_and_type_map=data_and_type_map, data_object=data_object)
        return data_object
