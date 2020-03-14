import os
from unittest.mock import patch

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


def test_overrides():
    env = {"SERVICE_VAR": "booking"}
    with patch.dict(os.environ, env):
        config = Inherit("./tests/test.env", override=True)
    assert config.SERVICE_VAR == "my-app"


def test_dont_override():
    env = {"SERVICE_VAR": "booking"}
    with patch.dict(os.environ, env):
        config = Inherit("./tests/test.env")
    assert config.SERVICE_VAR == "booking"


@pytest.fixture
def mock_failure(monkeypatch):
    monkeypatch.setenv("THIS_ONE", "dev")


def test_raise_infomative_error(mock_failure):
    class ErrConf(EnvConfig):
        THIS_ONE = param.Int(required=True)

    with pytest.raises(ValueError) as err:
        ErrConf()

    assert (
        "Config param 'THIS_ONE' expected 'Int', received "
        "invalid literal for int() with base 10: 'dev'"
    ) in str(err)
