from flask import Flask, jsonify

from envconfig import param
from envconfig import EnvConfig


class DefaultAppConfig(EnvConfig):
    """App env config."""

    HOST = param.Str(required=True)
    PORT = param.Int(required=True)
    PASSWORD = param.Str(override="SECRET_REDIS_PW", required=True)


class AppConfig(DefaultAppConfig):

    SERVICE = param.Str(prefix="MY_APP_")
    VERSION = param.Int(default=1)
    ENV = param.Str(default="prod")
    REMOTE_HOST = param.Int(default=0)


app = Flask(__name__)
env = AppConfig(env_path=".env")

app.config.from_object(env)


@app.route("/healthcheck")
def healthcheck():
    """ Application healthcheck."""
    return jsonify(version=app.config["VERSION"], environment=app.config["ENV"],)


# DefaultAppConfig
config = DefaultAppConfig()
print(config.HOST)
print(config["HOST"])

# AppConfig
print(env.HOST)
print(env["HOST"])
print(env["REMOTE_HOST"])
print(env["VERSION"])



app.run(debug=True)
