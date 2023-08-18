import os
from os import environ

WERKZEUG_DEBUG_PIN = os.environ.get("WERKZEUG_DEBUG_PIN")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")