import logging
from os.path import join

import easyappdirs
from logzero import logger, loglevel, logfile

loglevel(logging.ERROR)

VERSION = "0.1"
APP_NAME = "crypto2fiat"
AUTHOR = "Raphael Nanje"

dirs = easyappdirs.EasyAppDirs(APP_NAME, AUTHOR)

logfile(join(dirs.user_log_dir, "logs.log"))

dirs.register_config_file("settings.json", "settings")
dirs.register_config_file("settings.json.example", "default-settings")
dirs.register_data_file("coin_ids.json", "ids")
dirs.register_cache_file("metadata.json", "metadata")
dirs.register_cache_file("coin_data_cache.json", "data")


class Settings:

    def __init__(self) -> None:
        # the maximum amount of minutes before refreshing data
        self.CACHE_REFRESH_TIME = 10
        # thee default currency
        self.DEFAULT_FIAT = "USD"

    def load(self, d):
        for key, value in d.items():
            setattr(self, key, value)


settings = Settings()

logger.debug("Loading settings file")
if dirs.exists("settings"):
    logger.debug("Loading user settings file")
    settings.load(dirs.load("settings"))

elif dirs.exists("default-settings"):
    logger.debug("Loading default settings file")
    settings.load(dirs.load("default-settings"))

else:
    logger.debug("Creating new default settings file")
    dirs.save("default-settings", settings.__dict__)
