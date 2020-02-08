import os


class Param:

    TYPE_MAPPING = {
        "Int": int,
        "Str": str,
    }

    def __init__(self, override=None, default=None, required=False, prefix=None):
        self.override = override
        self.prefix = prefix
        self.default = default if default else ""
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
        return self.TYPE_MAPPING[self.__class__.__name__](value)


class Int(Param):
    pass


class Str(Param):
    pass
