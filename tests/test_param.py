import pytest

from envconf import param


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("THIS_ONE", "dev")
    monkeypatch.setenv("HOST", "localhost")
    monkeypatch.setenv("NUMBER", "60")


def test_override(mock_env):
    p = param.Str(override="THIS_ONE")
    value = p("HOST")
    assert value == "dev"


def test_default(mock_env):
    p = param.Str(default="DEBUG")
    value = p("LOG_LEVEL")
    assert value == "DEBUG"


def test_required(mock_env):
    p = param.Str(required=True)
    with pytest.raises(KeyError):
        p("LOG_LEVEL")


def test_not_required(mock_env):
    p = param.Str()
    value = p("PASSWORD")
    assert not value


def test_prefix(mock_env):
    p = param.Str(prefix="THIS_")
    value = p("ONE")
    assert value == "dev"


def test_type_mapping_int(mock_env):
    integer = param.Int()
    value = integer("NUMBER")
    assert value == 60
    assert type(value) is int
