from toolz import dissoc
from toolz import itemfilter
from dotenv import load_dotenv

from envconf.param import Param


def is_param(item):
    k, v = item
    return isinstance(v, Param)


class EnvConfigMeta(type):
    def __new__(metacls, cls_name, bases, attrs):
        klass = super().__new__(metacls, cls_name, bases, attrs)
        # Add all params to klass.opts attribute
        klass.opts = itemfilter(is_param, attrs)
        return klass


class EnvConfig(metaclass=EnvConfigMeta):
    def __init__(self, env_path=None):
        self.env_path = env_path
        load_dotenv(dotenv_path=env_path)
        self._init_fields()

    def _init_fields(self) -> None:
        remove = []
        for key, attr in self.opts.items():
            var = attr(key)
            setattr(self, key, var) if var else remove.append(key)

        self.opts = dissoc(self.opts, *remove)

    def __getitem__(self, name):
        return getattr(self, name)
