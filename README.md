<h1 align='center'>
    py-envconfig ⚙️
</h1>

<h4 align='center'>
    Managing config data from the environment, inspired by envconfig
</h4>

[envconfig](https://github.com/kelseyhightower/envconfig)

## Install

```
pip install py-envconfig
```

## Usage

Set some environment variable, or write a `.env` file.

```bash
HOST=localhost
PORT=6000

MY_APP_SERVICE=bookings
RELEASE_NUMBER=12
ENV=dev
```

Then specify your config:

```python
from envconfig import param
from envconfig import EnvConfig


class AppConfig(EnvConfig):
    """App env config."""

    HOST = param.Str(required=True)
    PORT = param.Int(required=True)
    PASSWORD = param.Str(override="SECRET_REDIS_PW", required=True)

    SERVICE = param.Str(prefix="MY_APP_")
    VERSION = param.Int(override="RELEASE_NUMBER")
    ENV = param.Str(default="prod")


config = AppConfig()

# Access by class attribute or subscript
config.USER
config["USER"]
```

Setup flask config:

```python
config = AppConfig()
app.config.from_object(config)
```

Point to a `.env` file

```python
config = AppConfig("./.env")
```

## Development

### Testing

```
pytest tests/
```

### Package and Distributing

Create package

```bash
rm -rf dist/
python setup.py sdist bdist_wheel
```

Upload to package index

```bash
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
