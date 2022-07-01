import inspect


class JYUtil:

    @staticmethod
    def get_class_attrs(class_or_object) -> dict:
        name_and_data_type = {}
        for attrs in inspect.getmembers(class_or_object):
            if len(attrs) == 2 and attrs[0] == "__annotations__":
                for attr_name in attrs[1]:
                    name_and_data_type[attr_name] = attrs[1][attr_name].__name__
                break
        return name_and_data_type
