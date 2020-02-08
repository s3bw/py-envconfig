import pytest

from envconf import param
from envconf import EnvConfig


class EnvTestConfig(EnvConfig):

    TEST_VAR = param.Int(default=45)
    NEW_VAR = param.Str(override="SET_THIS_VAR")


@pytest.mark.parametrize("key, expected", [("TEST_VAR", 123), ("NEW_VAR", "env")])
def test_getitem(key, expected):
    config = EnvTestConfig("./tests/test.env")

    assert config[key] == expected
    assert getattr(config, key) == expected
