<h1 align='centre'>
    py-envconfig ⚙️
</h1>

<h4 align='centre'>
    Managing config data from the environment, similar to [envconfig](https://github.com/kelseyhightower/envconfig)
</h4>

## Install

```
pip install py-envconf
```

## Usage

Set some environment variable, or write a `.env` file.

```bash
HOST=localhost
PORT=6000
ENV=dev
```

Then specify your config:

```python
from envconf import param
from envconf import EnvConfig


class AppConfig(EnvConfig):
    """App env config."""

    HOST = param.Str(required=True)
    PORT = param.Int(required=True)
    PASSWORD = param.Str(override="SECRET_REDIS_PW", required=True)

    SERVICE = param.Str(prefix="MY_APP_")
    VERSION = param.Int(default=1)
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
