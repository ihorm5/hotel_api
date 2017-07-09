import os
import importlib

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

settings = importlib.import_module(os.getenv('TORNADO_SETTINGS_MODULE',
                                   'settings.development'))
