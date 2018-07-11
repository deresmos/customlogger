import logging
import os
from datetime import datetime
from os.path import expanduser

from colorlog import ColoredFormatter

from customlogger.only_filter import OnlyFilter
from customlogger.run_rotating_handler import RunRotatingHandler


class CustomLogger:
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    _ALL_LOG_FILENAME = 'all.log'
    _LOG_DIRPATH = './log'
    _STREAM_LEVEL = WARNING
    _FILE_LEVEL = DEBUG
    isSaveLog = False
    isColorLog = True
    _BACKUP_COUNT = 5

    _FILE_FMT = ('%(asctime)s %(levelname)s %(filename)s %(name)s '
                 '%(lineno)s "%(message)s"')
    _STREAM_FMT = '%(levelname)-8s %(message)s'
    _STREAM_DEBUG_FMT = ('[%(levelname)s: File "%(filename)s", '
                         'line %(lineno)s, in %(funcName)s] "%(message)s"')
    _STREAM_COLOR_FMT = '%(log_color)s%(levelname)-8s%(reset)s %(message)s'
    _STREAM_COLOR_DEBUG_FMT = ('[%(log_color)s%(levelname)s%(reset)s: '
                               'File "%(filename)s", line %(lineno)s, '
                               'in %(funcName)s] "%(message)s"')
    _DATE_FMT = '%Y-%m-%d %a %H:%M:%S'

    logColors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }

    @classmethod
    def debugMode(cls):
        cls._STREAM_LEVEL = CustomLogger.DEBUG

    @classmethod
    def backupCount(cls, value):
        cls._BACKUP_COUNT = value

    @property
    def logger(self):
        if not self.__logger.handlers or self.__isFirstInitLogger:
            self.setLogger()

        return self.__logger

    @property
    def logDirPath(self):
        return self.log_dirpath

    @logDirPath.setter
    def logDirPath(self, path):
        path = expanduser(path)
        path = datetime.now().strftime(path)
        self.log_dirpath = path

    def __init__(
            self,
            parent=None,
            logger_name=None,
            is_default=True,
            is_debug=False,
            *,
            stream_level=None,
            backup_count=None,
            log_dirpath=None,
    ):
        name = parent or self
        name = logger_name or type(name).__name__
        logger = logging.getLogger(name)
        self.__logger = logger

        self.stream_level = stream_level or CustomLogger._STREAM_LEVEL
        self.backup_count = backup_count or CustomLogger._BACKUP_COUNT
        self.log_dirpath = log_dirpath or CustomLogger._LOG_DIRPATH

        self.is_default = is_default
        if is_debug:
            self.stream_level = self.DEBUG

        self.__isFirstInitLogger = True
        if self.__logger.handlers:
            self.__isFirstInitLogger = False

    @staticmethod
    def __createLogDir(path):
        path = expanduser(path)
        if os.path.isdir(path):
            return

        os.makedirs(path)

    def setLogger(self):
        if self.is_default:
            self.defaultLoggerSetting()

    def defaultLoggerSetting(self):
        self.__logger.setLevel(CustomLogger.DEBUG)
        if self.isColorLog:
            if self.stream_level <= self.DEBUG:
                fmt = self._STREAM_COLOR_DEBUG_FMT
            else:
                fmt = self._STREAM_COLOR_FMT

            self.addStreamColorHandler(self.stream_level, fmt=fmt)
        else:
            if self.stream_level <= self.DEBUG:
                fmt = self._STREAM_DEBUG_FMT
            else:
                fmt = self._STREAM_FMT

            self.addStreamHandler(self.stream_level, fmt=fmt)

        self.addStreamHandler(
            CustomLogger.INFO, is_only=True, check_level=True)
        if self.isSaveLog:
            self.__createLogDir(self.log_dirpath)
            self.addFileHandler(self._FILE_LEVEL)
            self.addRunRotatingHandler(CustomLogger.DEBUG, self.backup_count)

    def addHandler(
            self,
            handler,
            level,
            fmt=None,
            datefmt=None,
            is_only=False,
            formatter=None,
    ):
        handler.setLevel(level)

        datefmt = datefmt or self._DATE_FMT
        formatter = formatter or logging.Formatter(fmt, datefmt)
        handler.setFormatter(formatter)

        # set only filter
        if is_only:
            handler.addFilter(OnlyFilter(level))

        self.__logger.addHandler(handler)

    def addStreamHandler(self,
                         level,
                         fmt=None,
                         is_only=False,
                         check_level=False):
        if check_level and self.stream_level <= level:
            return

        handler = logging.StreamHandler()
        self.addHandler(handler, level, fmt=fmt, is_only=is_only)

    def addStreamColorHandler(self,
                              level,
                              fmt=None,
                              is_only=False,
                              check_level=False):
        if check_level and self.stream_level <= level:
            return

        handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            fmt,
            log_colors=self.logColors,
            style='%',
        )
        self.addHandler(handler, level, is_only=is_only, formatter=formatter)

    def addFileHandler(self, level, out_path=None, fmt=None, is_only=False):
        out_path = expanduser(
            out_path or os.path.join(self.log_dirpath, self._ALL_LOG_FILENAME))
        handler = logging.FileHandler(out_path)
        fmt = fmt or self._FILE_FMT
        self.addHandler(handler, level, fmt, is_only)

    def addRotatingFileHandler(self,
                               level,
                               out_path,
                               max_bytes,
                               backup_count,
                               fmt=None,
                               is_only=False):
        handler = logging.handlers.RotatingFileHandler(
            filename=out_path,
            maxBytes=max_bytes,
            backup_count=backup_count,
        )
        fmt = fmt or self._FILE_FMT
        self.addHandler(handler, level, fmt, is_only)

    def addRunRotatingHandler(self,
                              level,
                              backup_count,
                              out_path=None,
                              fmt=None,
                              is_only=False):
        out_path = expanduser(out_path or self.log_dirpath)
        handler = RunRotatingHandler(out_path, backup_count)
        fmt = fmt or self._FILE_FMT
        self.addHandler(handler, level, fmt, is_only)
