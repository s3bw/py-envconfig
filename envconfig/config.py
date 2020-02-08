from toolz import dissoc
from toolz import itemfilter
from dotenv import load_dotenv

from envconfig.param import Param


def _is_param(item):
    k, v = item
    return isinstance(v, Param)


class EnvConfigMeta(type):
    def __new__(metacls, cls_name, bases, attrs):
        klass = super().__new__(metacls, cls_name, bases, attrs)
        # Add all params to klass.params attribute
        klass.params = itemfilter(_is_param, attrs)
        return klass


class EnvConfig(metaclass=EnvConfigMeta):
    def __init__(self, env_path=None):
        self.env_path = env_path
        load_dotenv(dotenv_path=env_path)
        self._init_fields()

    def _init_fields(self) -> None:
        remove = []
        for key, attr in self.params.items():
            var = attr(key)
            setattr(self, key, var) if var else remove.append(key)

        self.params = dissoc(self.params, *remove)

    def __getitem__(self, name):
        return getattr(self, name)
