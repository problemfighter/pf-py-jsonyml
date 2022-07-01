from pf_py_jsonyml.common.jy_util import JYUtil
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
