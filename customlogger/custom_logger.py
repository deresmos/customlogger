# imports {{{1
import logging
import os

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

    logFileName = 'all.log'
    logDirPath = './log'
    streamLevel = WARNING
    isSaveLog = False
    backupCount = 5
    fileLogFmt = '%(asctime)s %(filename)s %(name)s '\
        '%(lineno)s %(levelname)s "%(message)s"'
    streamLogFmt = '[%(levelname)s: File "%(filename)s", ' \
        'line %(lineno)s, in %(funcName)s] "%(message)s"'

    __loggerLists = []

    # class methods {{{1
    # debugMode {{{2

    @classmethod
    def debugMode(cls):
        cls.streamLevel = CustomLogger.DEBUG

    # setStreamLevel {{{2
    @classmethod
    def setStreamLevel(cls, level):
        cls.streamLevel = level

    # saveLog {{{2
    @classmethod
    def saveLog(cls):
        cls.isSaveLog = True

    # setLogDirPath {{{2
    @classmethod
    def setLogDirPath(cls, path):
        cls.logDirPath = path

    # setLogFileName {{{2
    @classmethod
    def setLogFileName(cls, filename):
        cls.logFileName = filename

    # setFileFmt {{{2
    @classmethod
    def setFileFmt(cls, fmt):
        cls.fileLogFmt = fmt

    # setStreamFmt {{{2
    @classmethod
    def setStreamFmt(cls, fmt):
        cls.streamLogFmt = fmt

    # property {{{1
    @property
    def logger(self):
        return self.__logger

    # private functions {{{1
    def __init__(  # {{{2
            self, parent=None, logger_name=None, default=True):
        name = parent or self
        name = logger_name or type(name).__name__
        logger = logging.getLogger(name)
        self.__logger = logger

        if self.__checkLoggerLists(logger) or not default:
            return

        self.defaultLoggerSetting()

    @staticmethod  # __checkLoggerLists {{{2
    def __checkLoggerLists(logger):
        id_ = id(logger)
        if id_ in CustomLogger.__loggerLists:
            return True

        CustomLogger.__loggerLists.append(id_)
        return False

    @staticmethod  # __createLogDir {{{2
    def __createLogDir(path=None):
        path = path or CustomLogger.logDirPath
        if os.path.isdir(path):
            return

        os.mkdir(path)
        print('Create log directory. ({})'.format(os.path.abspath(path)))

    # public functions {{{1
    def defaultLoggerSetting(self):  # {{{2
        self.__logger.setLevel(CustomLogger.DEBUG)
        fmt = self.streamLogFmt
        self.addStreamHandler(CustomLogger.streamLevel, fmt=fmt)
        self.addStreamHandler(
            CustomLogger.INFO, is_only=True, check_level=True)

        if CustomLogger.isSaveLog:
            self.__createLogDir()
            self.addFileHandler(CustomLogger.DEBUG)
            self.addRunRotatingHandler(CustomLogger.DEBUG,
                                       CustomLogger.backupCount)

    def addHandler(  # {{{2
            self, handler, level, fmt=None, datefmt=None, is_only=False):
        handler.setLevel(level)

        datefmt = datefmt or '%Y-%m-%d %a %H:%M:%S'
        handler.setFormatter(logging.Formatter(fmt, datefmt))

        # set only filter
        if is_only:
            handler.addFilter(OnlyFilter(level))

        self.__logger.addHandler(handler)

    def addStreamHandler(  # {{{2
            self, level, fmt=None, is_only=False, check_level=False):
        if check_level and CustomLogger.streamLevel <= level:
            return

        handler = logging.StreamHandler()
        self.addHandler(handler, level, fmt=fmt, is_only=is_only)

    def addFileHandler(  # {{{2
            self, level, out_path=None, fmt=None, is_only=False):
        out_path = out_path or os.path.join(CustomLogger.logDirPath,
                                            CustomLogger.logFileName)
        handler = logging.FileHandler(out_path)
        fmt = fmt or CustomLogger.fileLogFmt
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
        fmt = fmt or CustomLogger.fileLogFmt
        self.addHandler(handler, level, fmt, is_only)

    def addRunRotatingHandler(  # {{{2
            self,
            level,
            backup_count,
            out_path=None,
            fmt=None,
            is_only=False):
        out_path = out_path or CustomLogger.logDirPath
        handler = RunRotatingHandler(out_path, backup_count)
        fmt = fmt or CustomLogger.fileLogFmt
        self.addHandler(handler, level, fmt, is_only)


# }}}1

#  main {{{1
if __name__ == '__main__':
    CustomLogger.setLogDirPath('./log')
    CustomLogger.setStreamLevel(CustomLogger.ERROR)
    CustomLogger.saveLog()
    # CustomLogger.isSaveLog = True
    logger = CustomLogger()
    logger = logger.logger
    logger.error('aaa')
    logger.debug('debug test')
    logger.info('info test')
    logger.warning('warning test')
    logger1 = CustomLogger(logger_name='logger name').logger
    logger1.info('info test2')
