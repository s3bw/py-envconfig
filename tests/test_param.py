from datetime import datetime, timedelta, timezone

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
    monkeypatch.setenv("DATETIME", "2022-06-16T18:35:13+12:00")
    monkeypatch.setenv("DATETIME_2", "2022-06-16 18:35:13")
    monkeypatch.setenv("DATETIME_2_FORMAT", "%Y-%m-%d %H:%M:%S")
    monkeypatch.setenv("TIMEDELTA_DAYS", "1")


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


def test_datetime_public_type():
    d = param.Datetime()
    assert d.type == "Datetime"


def test_datetime_parse():
    d = param.Datetime()
    value = d("DATETIME")
    assert value == datetime(2022, 6, 16, 18, 35, 13, tzinfo=timezone(12))


def test_datetime_parse_2():
    d = param.Datetime()
    value = d("DATETIME_2")
    assert value == datetime(2022, 6, 16, 18, 35, 13, tzinfo=timezone(12))


def test_timedelta():
    t = param.Timedelta()
    value = t("TIMEDELTA_DAYS")
    assert value.total_seconds() == 86400


def test_timedelta_default_int():
    t = param.Timedelta(default=7)
    value = t("TIMEDELTA_NOT_DEFINED_HOURS")
    assert isinstance(value, timedelta)
    assert value.total_seconds() = 7 * 24 * 3600


def test_timedelta_default_float():
    t = param.Timedelta(default=7.0)
    value = t("TIMEDELTA_NOT_DEFINED_MINUTES")
    assert isinstance(value, timedelta)
    assert value.total_seconds() == 7.0 * 60


def test_timedelta_default_timedelta():
    t = param.Timedelta(default=timedelta(seconds=30))
    value = t("TIMEDELTA_NOT_DEFINED_SECONDS")
    assert isinstance(value, timedelta)
    assert value.total_seconds() == 30


def test_timedelta_default_timedelta_2():
    t = param.Timedelta(default=timedelta(seconds=30))
    value = t("TIMEDELTA_NOT_DEFINED_HOURS")
    assert isinstance(value, timedelta)
    assert value.total_seconds() == 30
