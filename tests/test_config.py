import pytest

from envconfig import param
from envconfig import EnvConfig


class EnvTestConfig(EnvConfig):

    TEST_VAR = param.Int(default=45)
    NEW_VAR = param.Str(override="SET_THIS_VAR")


@pytest.mark.parametrize("key, expected", [("TEST_VAR", 123), ("NEW_VAR", "env")])
def test_getitem(key, expected):
    config = EnvTestConfig("./tests/test.env")

    assert config[key] == expected
    assert getattr(config, key) == expected


class Inherit(EnvTestConfig):

    SERVICE_VAR = param.Str()
    REMOTE_HOST = param.Str(default="no-host")


@pytest.mark.parametrize(
    "key, expected",
    [
        ("TEST_VAR", 123),
        ("NEW_VAR", "env"),
        ("SERVICE_VAR", "my-app"),
        ("REMOTE_HOST", "no-host"),
    ],
)
def test_inherited_getitem(key, expected):
    config = Inherit("./tests/test.env")

    assert config[key] == expected
    assert getattr(config, key) == expected
