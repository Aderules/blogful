import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
if os.environ.get("TRAVIS"):
    # CJA 20160403: Travis doesn't set env vars properly.
    config_path = "blog.config.TravisConfig"


app.config.from_object(config_path)

from . import views
from . import filters
from . import login