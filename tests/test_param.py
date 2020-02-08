import pytest

from envconfig import param


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("THIS_ONE", "dev")
    monkeypatch.setenv("HOST", "localhost")
    monkeypatch.setenv("NUMBER", "60")
    monkeypatch.setenv("ACTIVATE_FEATURE", "true")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("false", False),
        ("False", False),
        ("f", False),
        ("no", False),
        ("No", False),
        ("never", False),
        (":(", False),
        ("n", False),
        ("0", False),
        (0, False),
        ("t", True),
        ("true", True),
        ("True", True),
        ("y", True),
        ("yes", True),
        ("1", True),
        (1, True),
    ],
)
def test_boolean_cast(value, expected):
    result = param._boolean(value)
    assert result is expected


def test_boolean_param(mock_env):
    p = param.Bool()
    value = p("ACTIVATE_FEATURE")
    assert value is True


def test_boolean_default(mock_env):
    p = param.Bool(default="f")
    value = p("ACTIVE")
    assert value is False


def test_override(mock_env):
    p = param.Str(override="THIS_ONE")
    value = p("HOST")
    assert value == "dev"


def test_default(mock_env):
    p = param.Str(default="DEBUG")
    value = p("LOG_LEVEL")
    assert value == "DEBUG"


def test_default_to_zero(mock_env):
    p = param.Int(default=0)
    value = p("LOG_LEVEL")
    assert value is not None
    assert value == 0


def test_required(mock_env):
    p = param.Str(required=True)
    with pytest.raises(KeyError) as e_info:
        p("LOG_LEVEL")
    assert "LOG_LEVEL" in str(e_info)


def test_required_prefix(mock_env):
    p = param.Str(required=True, prefix="MY_FIRST_")
    with pytest.raises(KeyError) as e_info:
        p("APP")
    assert "MY_FIRST_APP" in str(e_info)


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
