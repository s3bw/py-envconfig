import os
from abc import ABC, abstractmethod

from enum import Enum as pyEnum


class Types(pyEnum):
    Str = "Str"
    Int = "Int"
    Bool = "Bool"
    Enum = "Enum"
    Float = "Float"
    Config = "Config"


def _boolean(value):
    return str(value).lower() in ["true", "1", "t", "y", "yes"]


class Param(ABC):
    def __init__(self, override=None, default=None, required=False, prefix=None):
        self.override = override
        self.prefix = prefix
        self.default = default
        self.required = required

    def __call__(self, name):
        # Some environment variables will be prefixed
        # this will return env var with prefix + name
        if not self.override:
            name = self.prefix + name if self.prefix else name
        else:
            name = self.override

        if not self.required:
            value = os.getenv(name, self.default)
        else:
            try:
                value = os.environ[name]
            except KeyError:
                raise KeyError(f"Could not find '{name}' in environment.")

        # '_cast_' contains a method to cast to
        # an appropriate type decide by the class
        if value is not None:
            return self._cast(value)

    @abstractmethod
    def _cast(self, value):
        raise NotImplemented

    @property
    def _type_(self):
        """Params are represented by their type."""
        return Types(self.__class__.__name__)

    def __eq__(self, other):
        """Compare the param by it's type."""
        return self._type_ == other

    @property
    def type(self):
        """Public type for param represented by it's value."""
        return self._type_.value


class Bool(Param):
    def _cast(self, value):
        return _boolean(value)


class Int(Param):
    def _cast(self, value):
        return int(value)


class Str(Param):
    def _cast(self, value):
        return str(value)


class Enum(Param):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        super().__init__(**kwargs)

    def _cast(self, value):
        return self.enum(value)


class Float(Param):
    def _cast(self, value):
        return float(value)


class Config(Param):
    def __init__(self, cls, default=None):
        self.cls = cls
        self.default = default

    def __call__(self, _name):
        try:
            value = self.cls()
            return value
        except KeyError:
            return self.default
