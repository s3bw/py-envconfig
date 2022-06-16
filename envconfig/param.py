import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from enum import Enum as pyEnum


class Types(pyEnum):
    Str = "Str"
    Int = "Int"
    Bool = "Bool"
    Enum = "Enum"
    Float = "Float"
    Datetime = "Datetime"
    Timedelta = "Timedelta"


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


class Datetime(Param):
    def __init__(self, format_suffix: str = "_FORMAT", format_override: str = None, format_default: str = "%Y-%m-%dT%H:%M:%S%z", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_suffix = format_suffix
        self.format_override = format_override
        self.format_default = format_default

    def __call__(self, name):
        # Some environment variables will be prefixed
        # this will return env var with prefix + name
        if not self.override:
            name = self.prefix + name if self.prefix else name
        else:
            name = self.override

        if not self.format_override:
            format_name = name + self.format_suffix
        else:
            format_name = self.format_override

        value_format = os.getenv(format_name, self.format_default)

        if name in os.environ:
            value_str = os.environ[name]
            value = datetime.strptime(value_str, value_format)

        elif self.required:
            raise KeyError(f"Could not find '{name}' in environment.")

        elif isinstance(self.default, str):
            value = datetime.strptime(self.default, value_format)
        else:
            value = self.default

        return value


class Timedelta(Param):
    def __init__(self, units, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, name):
        value = super().__call__(name)
        try:
            converted = int(value)
        except:
            converted = float(value)

        units = name.split('_')[-1].lower()
        td = timedelta(**{units: converted})
        return td
