from pydantic import BaseSettings

from typing import get_type_hints, get_args


def create_dynamic_class(class_name, field_name, default_value, annotations, config=None):
    # 定义类属性字典
    class_attrs = {
        field_name: None,  # 这里可以根据需要添加更多的类属性,
        "__annotations__": annotations
    }
    if config is not None:
        class_attrs['Config'] = config

    # 使用type函数创建类
    dynamic_class = type(class_name, (BaseSettings,), class_attrs)
    return dynamic_class


class ExternalSourceConfig:
    def __init__(self, get_from_external, validation_alias: str = None, *, default_value=None):
        self.get_from_external = get_from_external
        self.validation_alias = validation_alias
        self.default_value = default_value

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        """
        the value will not be modified from external call
        :param instance:
        :param value:
        :return:
        """
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self

        type_ = get_args(get_type_hints(owner)[self.name])[0]
        annotations = {self.name: type_}
        setting_class = create_dynamic_class(owner.__name__ + self.__class__.__name__,
                                             self.name,
                                             self.default_value,
                                             annotations,
                                             owner.Config)
        setting_instance = setting_class()
        if getattr(setting_instance, self.name) is not None:
            return getattr(setting_instance, self.name)

        key = self.validation_alias if self.validation_alias is not None else self.name
        setting_value = self.get_from_external(key)
        return setting_value if setting_value else self.default_value
