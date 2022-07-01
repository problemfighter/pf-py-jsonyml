from pf_py_jsonyml.common.jy_util import JYUtil
from pf_py_jsonyml.jybase import JYBase


class ObjectDict:

    def get_dict(self, data_object: JYBase):
        response_dict = {}
        data_and_type_map = JYUtil.get_class_attrs(data_object)
        for field_name in data_and_type_map:
            data = None
            if hasattr(data_object, field_name):
                data = getattr(data_object, field_name)
                if isinstance(data, JYBase):
                    data = self.get_dict(data)
            response_dict[field_name] = data
        return response_dict
