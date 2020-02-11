from toolz import merge
from toolz import itemfilter
from dotenv import load_dotenv

from envconfig.param import Param


def _is_param(item):
    k, v = item
    return isinstance(v, Param)


class EnvConfigMeta(type):
    def __new__(metacls, cls_name, bases, attrs):
        klass = super().__new__(metacls, cls_name, bases, attrs)

        # Construct params from inherited class
        _params_ = {}
        for base in bases:
            if hasattr(base, "params"):
                _params_ = merge(base.params, _params_)

        # Add all params to klass.params attribute
        klass.params = merge(itemfilter(_is_param, attrs), _params_)
        return klass


class EnvConfig(metaclass=EnvConfigMeta):
    def __init__(self, env_path=None, override=False, verbose=False):
        self.env_path = env_path
        load_dotenv(dotenv_path=env_path, override=override, verbose=verbose)
        self._init_fields()

    def _init_fields(self) -> None:
        """Set self.params as attributes."""
        for key, attr in self.params.items():
            var = attr(key)
            setattr(self, key, var)

    def __getitem__(self, name):
        return getattr(self, name)
