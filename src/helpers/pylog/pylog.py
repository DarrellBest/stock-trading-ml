#!/usr/bin/env python
"""
PyLog is a wrapper for the Python logging library
It implements a custom thread-safe singleton and can be
called safely on multiple threads.
PyLog will work for Python 2 or 3.

To use, Simply import like so:
  from pylog import PyLog

Then, get an instance:
  log = PyLog.Instance().log

You can then call
    log.debug('message')
    log.info('message')
    log.warning('message')
    log.error('message')
    log.critical('message')

set DEBUG to True to see __log.debug messages
all other messages will be seen regardless
"""

__author__ = "Darrell Best"
__copyright__ = "Copyright 2018, MTEQ"
__credits__ = ["Darrell Best, John Burton, Thomas Moulton"]
__version__ = "1.0.0"
__maintainer__ = "Darrell Best"
__email__ = "dbest@mteq.com"
__status__ = "Development"


import logging
import pathlib
from helpers.singleton.singleton import Singleton
from logging.handlers import TimedRotatingFileHandler
from time import localtime, strftime
from colorlog import ColoredFormatter
from configparser import ConfigParser


@Singleton
class PyLog:
    """
    Custom Python Logger class taking advantage of default Python Logging.
    """
    # TODO ADD LEVEL ARG PARAM
    def __init__(self):
        settings = ConfigParser()
        settings.read('configs/settings.ini')

        self.__colored_formatter = ColoredFormatter(
            "%(log_color)s%(levelname)s " + "%(reset)s" + "%(white)s %(asctime)s " + "%(white)s["
            + "%(yellow)s%(filename)s" + "%(white)s: " + "%(cyan)s%(threadName)s" + "%(white)s: "
            + "%(purple)s%(funcName)s()" + "%(white)s: " + "%(green)s%(lineno)s" + "%(white)s]"
            + "%(log_color)s: %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red',
            }
        )
        self.__file_log_formatter = "%(levelname)s " + " %(asctime)s " + "[" + "%(filename)s" + ": " \
                                    + "%(threadName)s" + ": " + "%(funcName)s()" + ": " \
                                    + "%(lineno)s" + "]" + ": %(message)s"

        if settings.has_option('LOGGING', 'logging_dir'):
            self.__directory = settings.get('LOGGING', 'logging_dir')
        else:
            self.__directory = "./log"
        pathlib.Path(self.__directory).mkdir(exist_ok=True)
        self.__filename = self.__directory + strftime("/%Y-%m-%d.log", localtime())
        self.__log = logging.getLogger("PyLog")

        if settings.has_option('LOGGING', 'logging_level'):
            self.__log.setLevel(logging.getLevelName(settings.get('LOGGING', 'logging_level')))
        else:
            self.__log.setLevel(logging.getLevelName(logging.INFO))

        self.__handler = TimedRotatingFileHandler(self.__filename, when='h', interval=1, backupCount=5)
        self.__handler.setFormatter(logging.Formatter(self.__file_log_formatter))
        self.__log.addHandler(self.__handler)

        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setFormatter(self.__colored_formatter)
        self.__log.addHandler(self.__stream_handler)

    @property
    def log(self):
        return self.__log
