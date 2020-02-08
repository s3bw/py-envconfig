import os

from enum import Enum


class Types(Enum):
    Str = "Str"
    Int = "Int"
    Bool = "Bool"


def _boolean(value):
    return str(value).lower() in ["true", "1", "t", "y", "yes"]


class Param:

    TYPE_MAPPING = {
        Types.Int: int,
        Types.Str: str,
    }

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

        # TYPE_MAPPING contains a mapping of class name
        # to type this will cast the env var as the type
        # set by the class
        if value is not None:
            return self._cast_(value)

    def _cast_(self, value):
        if self == Types.Bool:
            # Cast to boolean can't be done with
            # bool() since this returns True on
            # both bool("true") and bool("false")
            return _boolean(value)
        else:
            return self.TYPE_MAPPING[self._type_](value)

    @property
    def _type_(self):
        """Params are represented by their type."""
        return Types(self.__class__.__name__)

    def __eq__(self, other):
        """Compare the param by it's type."""
        return self._type_ == other


class Bool(Param):
    pass


class Int(Param):
    pass


class Str(Param):
    pass
