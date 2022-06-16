from enum import Enum

import pytest

from envconfig import param


class Colour(Enum):

    Blue = "blue"
    Yellow = "yellow"
    Red = "red"


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("THIS_ONE", "dev")
    monkeypatch.setenv("HOST", "localhost")
    monkeypatch.setenv("NUMBER", "60")
    monkeypatch.setenv("ACTIVATE_FEATURE", "true")
    monkeypatch.setenv("COLOUR_BLUE", "blue")
    monkeypatch.setenv("COLOUR_YELLOW", "yellow")
    monkeypatch.setenv("FLOAT_CONFIG", "3.141")
    monkeypatch.setenv("C1_STR", "C1")
    monkeypatch.setenv("C2_STR", "C2")
    monkeypatch.setenv("C3_STR", "C3")


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


@pytest.mark.parametrize(
    "value, expected",
    [
        ("COLOUR_YELLOW", Colour.Yellow),
        ("COLOUR_BLUE", Colour.Blue),
        ("THIS", Colour.Red),
    ],
)
def test_enum_param(value, expected, mock_env):
    p = param.Enum(Colour, default=Colour.Red)
    value = p(value)
    assert value is expected


def test_invalid_enum(mock_env):
    p = param.Enum(Colour)
    with pytest.raises(ValueError) as e_info:
        value = p("THIS_ONE")
    assert "'dev' is not a valid Colour" in str(e_info)


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


def test_invalid_type_error_int(mock_env):
    with pytest.raises(ValueError):
        p = param.Int()
        value = p("THIS_ONE")


def test_param_public_type():
    integer = param.Int()
    assert integer.type == "Int"


def test_float_public_type():
    f = param.Float()
    assert f.type == "Float"


def test_float_parse(mock_env):
    f = param.Float()
    value = f("FLOAT_CONFIG")
    assert value == 3.141
    assert type(value) is float


def test_config_public_type():
    c = param.Config(None)
    assert c.type == "Config"


def test_config_parse():
    class C1(EnvConfig):
        C1_STR = param.Str()

    class C2(EnvConfig):
        C2_STR = param.Str()
        C1 = param.Config(C1)

    c2 = C2()
    assert c2.C2_STR == "C2"
    assert c2.C1.C1_STR == "C1"


def test_config_parse_nested():
    class C1(EnvConfig):
        C1_STR = param.Str()

    class C2(EnvConfig):
        C2_STR = param.Str()
        C1 = param.Config(C1)

    class C3(EnvConfig):
        C3_STR = param.Str()
        C2 = param.Config(C2)

    c3 = C3()
    assert c3.C3_STR == "C3"
    assert c3.C2.C2_STR == "C2"
    assert c3.C2.C1.C1_STR == "C1"
