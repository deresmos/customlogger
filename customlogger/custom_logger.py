# imports {{{1
import logging
import os
from os.path import expanduser

from customlogger.only_filter import OnlyFilter
from customlogger.run_rotating_handler import RunRotatingHandler

# }}}


class CustomLogger:
    # class variable {{{1
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    allLogFileName = 'all.log'
    logDirPath = './log'
    streamLevel = WARNING
    fileLevel = DEBUG
    isSaveLog = False
    backupCount = 5
    fileLogFmt = '%(asctime)s %(filename)s %(name)s '\
        '%(lineno)s %(levelname)s "%(message)s"'
    streamLogFmt = '[%(levelname)s: File "%(filename)s", ' \
        'line %(lineno)s, in %(funcName)s] "%(message)s"'
    dateFmt = '%Y-%m-%d %a %H:%M:%S'

    __loggerLists = []

    # class methods {{{1
    # debugMode {{{2

    @classmethod
    def debugMode(cls):
        cls.streamLevel = CustomLogger.DEBUG

    # property {{{1
    @property
    def logger(self):
        if not self.__logger.handlers:
            self.setLogger()

        return self.__logger

    # private functions {{{1
    def __init__(  # {{{2
            self, parent=None, logger_name=None, default=True):
        name = parent or self
        name = logger_name or type(name).__name__
        logger = logging.getLogger(name)
        self.__logger = logger
        self.__default = default

    @staticmethod  # __checkLoggerLists {{{2
    def __checkLoggerLists(logger):
        id_ = id(logger)
        if id_ in CustomLogger.__loggerLists:
            return True

        CustomLogger.__loggerLists.append(id_)
        return False

    @staticmethod  # __createLogDir {{{2
    def __createLogDir(path):
        path = expanduser(path)
        if os.path.isdir(path):
            return

        os.mkdir(path)
        print('Create log directory. ({})'.format(os.path.abspath(path)))

    # public functions {{{1
    def setLogger(self):  # {{{2
        if self.__checkLoggerLists(self.__logger) or not self.__default:
            return

        self.defaultLoggerSetting()

    def defaultLoggerSetting(self):  # {{{2
        self.__logger.setLevel(CustomLogger.NOTSET)
        fmt = self.streamLogFmt
        self.addStreamHandler(self.streamLevel, fmt=fmt)
        self.addStreamHandler(
            CustomLogger.INFO, is_only=True, check_level=True)

        if self.isSaveLog:
            self.__createLogDir(self.logDirPath)
            self.addFileHandler(self.fileLevel)
            self.addRunRotatingHandler(CustomLogger.NOTSET, self.backupCount)

    def addHandler(  # {{{2
            self, handler, level, fmt=None, datefmt=None, is_only=False):
        handler.setLevel(level)

        datefmt = datefmt or self.dateFmt
        handler.setFormatter(logging.Formatter(fmt, datefmt))

        # set only filter
        if is_only:
            handler.addFilter(OnlyFilter(level))

        self.__logger.addHandler(handler)

    def addStreamHandler(  # {{{2
            self, level, fmt=None, is_only=False, check_level=False):
        if check_level and self.streamLevel <= level:
            return

        handler = logging.StreamHandler()
        fmt = fmt or self.streamLogFmt
        self.addHandler(handler, level, fmt=fmt, is_only=is_only)

    def addFileHandler(  # {{{2
            self, level, out_path=None, fmt=None, is_only=False):
        out_path = expanduser(out_path or self.allLogFileName)
        handler = logging.FileHandler(out_path)
        fmt = fmt or self.fileLogFmt
        self.addHandler(handler, level, fmt, is_only)

    def addRotatingFileHandler(  # {{{2
            self,
            level,
            out_path,
            max_bytes,
            backup_count,
            fmt=None,
            is_only=False):
        handler = logging.handlers.RotatingFileHandler(
            filename=out_path, maxBytes=max_bytes, backupCount=backup_count)
        fmt = fmt or self.fileLogFmt
        self.addHandler(handler, level, fmt, is_only)

    def addRunRotatingHandler(  # {{{2
            self,
            level,
            backup_count,
            out_path=None,
            fmt=None,
            is_only=False):
        out_path = expanduser(out_path or self.logDirPath)
        handler = RunRotatingHandler(out_path, backup_count)
        fmt = fmt or self.fileLogFmt
        self.addHandler(handler, level, fmt, is_only)


# }}}1

#  main {{{1
if __name__ == '__main__':
    CustomLogger.setLevel(CustomLogger.ERROR)
    logger = CustomLogger()
    logger = logger.logger
    logger.error('aaa')
    logger.debug('debug test')
    logger.info('info test')
    logger.warning('warning test')
    logger1 = CustomLogger(logger_name='logger name').logger
    logger1.info('info test2')
