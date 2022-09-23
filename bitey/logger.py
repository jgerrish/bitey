"""
Logger configuration and initialization.

This shows how applications can setup a custom logger for the bitey
emulation library.

To setup the logger, call the setup_logger() function.

>>> from bitey.logger import setup_logger
>>> setup_logger()
"""
import logging
from threading import Lock

logger_initialized = False
"""
A module-level variable indicating whether the logger has been initialized.
Do not modify this variable unless you have acquired the logger module
lock logger_initialized_lock
"""

LOGGER_INITIALIZED_LOCK = Lock()
"Lock that controls access to the logger_initialized variable"


def setup_logger():
    """Initialize the logger and configure it."""
    with LOGGER_INITIALIZED_LOCK:
        global logger_initialized
        if logger_initialized:
            logger = logging.getLogger("bitey")
            logger.warning("Logger already initialized")
            return

        # create logger
        logger = logging.getLogger("bitey")
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler("bitey.log")
        fh.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add formatter to file handler
        fh.setFormatter(formatter)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        # Change the logger_initialized variable so the logger is only
        # setup once
        logger_initialized = True
