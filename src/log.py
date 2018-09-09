import logging
import sys
import os

LOGGER = logging.getLogger()

if "LOG_LEVEL" in os.environ:
    LOGGER.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL")))
    LOGGER.warn("setting log level to %s" % os.environ.get("LOG_LEVEL"))
else:
    LOGGER.setLevel(logging.WARN)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))
LOGGER.addHandler(handler)

LOGGER.info("LOGGER INITIALIZED")
