from flask import Flask, jsonify

import param
from envconf import EnvConfig


class AppConfig(EnvConfig):
    """App env config."""

    HOST = param.Str(required=True)
    PORT = param.Int(required=True)
    PASSWORD = param.Str(override="SECRET_REDIS_PW", required=True)

    SERVICE = param.Str(prefix="MY_APP_")
    VERSION = param.Int(default=1)
    ENV = param.Str(default="prod")


app = Flask(__name__)
env = AppConfig(env_path=".env")

app.config.from_object(env)


@app.route("/healthcheck")
def healthcheck():
    """ Application healthcheck."""
    return jsonify(
        version=app.config["VERSION"],
        environment=app.config["ENV"],
    )


print(env.HOST)
print(env["HOST"])
app.run(debug=True)
