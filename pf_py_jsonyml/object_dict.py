from pf_py_jsonyml.common.jy_util import JYUtil, JYDataType
from pf_py_jsonyml.jybase import JYBase
from typing import List, Dict


class ObjectDict:

    def _process_value(self, data, is_ignore_none=False, exclude: list = None):
        if not data:
            return data
        if isinstance(data, JYBase):
            data = self.get_dict(data, is_ignore_none)
        elif isinstance(data, List):
            data = self._handle_internal_list(data, is_ignore_none=is_ignore_none)
        elif isinstance(data, Dict):
            data = self._handle_internal_dict(data, is_ignore_none=is_ignore_none)
        return data

    def _handle_internal_list(self, list_data, is_ignore_none=False, exclude: list = None):
        response = []
        for item in list_data:
            item = self._process_value(item, is_ignore_none)
            response.append(item)
        return response

    def _handle_internal_dict(self, dict_data, is_ignore_none=False, exclude: list = None):
        response = {}
        for item_name in dict_data:
            response[item_name] = self._process_value(dict_data[item_name], is_ignore_none)
        return response

    def get_dict(self, data_object: JYBase, is_ignore_none=False, exclude: list = None):
        response_dict = {}
        data_and_type_map = JYUtil.get_class_attrs(data_object)
        for field_name in data_and_type_map:
            if exclude and field_name in exclude:
                continue
            data = None
            if hasattr(data_object, field_name):
                data = getattr(data_object, field_name, None)
                data = self._process_value(data, is_ignore_none)

            if not is_ignore_none:
                response_dict[field_name] = data
            elif is_ignore_none and data:
                response_dict[field_name] = data
        return response_dict

    def _init_jy_object(self, data, class_name, data_object: JYBase, exclude: list = None):
        jy_base_object = JYUtil.get_py_base_class_object(class_name, data_object)
        if jy_base_object:
            return self.get_object(data, jy_base_object, exclude=exclude)
        return None

    def _init_jy_list_object(self, data_list: list, class_name, data_object: JYBase, exclude: list = None):
        jy_object_list = []
        for data in data_list:
            response = self._init_jy_object(data, class_name, data_object, exclude=exclude)
            if response:
                jy_object_list.append(response)
        if jy_object_list:
            return jy_object_list
        return None

    def _init_jy_dict_object(self, data_dict: dict, class_name, data_object: JYBase, exclude: list = None):
        jy_object_dict = {}
        for data_name in data_dict:
            response = self._init_jy_object(data_dict[data_name], class_name, data_object, exclude=exclude)
            if response:
                jy_object_dict[data_name] = response
        if jy_object_dict:
            return jy_object_dict
        return None

    def _set_value_to_object(self, data_name: str, data: dict, data_and_type_map: dict, data_object: JYBase, exclude: list = None):
        if data_name in data_and_type_map:
            jy_data_type: JYDataType = data_and_type_map[data_name]
            value = None
            collection_exclude = None
            collection_exclude_name = data_name + "_nested"
            if exclude and collection_exclude_name in exclude:
                collection_exclude = exclude[collection_exclude_name]
            if jy_data_type.name == "Dict" and jy_data_type.objectType == "JYBase" and isinstance(data[data_name], dict) and jy_data_type.collectionClass:
                value = self._init_jy_dict_object(data[data_name], jy_data_type.collectionClass, data_object, exclude=collection_exclude)
            elif jy_data_type.name == "List" and jy_data_type.objectType == "JYBase" and isinstance(data[data_name], list) and jy_data_type.collectionClass:
                value = self._init_jy_list_object(data[data_name], jy_data_type.collectionClass, data_object, exclude=collection_exclude)
            elif jy_data_type.objectType == "JYBase":
                value = self._init_jy_object(data[data_name], jy_data_type.name, data_object, exclude=exclude)
            else:
                value = data[data_name]

            if value and jy_data_type.name == "str":
                value = str(value)

            setattr(data_object, data_name, value)
        return data_object

    def get_object(self, data: dict, data_object: JYBase, exclude: list = None):
        if not data or not data_object:
            return None
        data_and_type_map = JYUtil.get_class_attrs(data_object)
        for item_name in data:
            if exclude and item_name in exclude:
                continue
            data_object = self._set_value_to_object(item_name, data=data, data_and_type_map=data_and_type_map, data_object=data_object, exclude=exclude)

        for attr in data_and_type_map:
            if not hasattr(data_object, attr):
                setattr(data_object, attr, None)
        return data_object
