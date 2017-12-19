import io
import logging

import pytest

from customlogger import CustomLogger


def pytest_report_header(config):
    return 'custom_logger test'


def test_default_params():  # {{{1
    assert CustomLogger.allLogFileName == 'all.log'
    assert CustomLogger.logDirPath == './log'
    assert CustomLogger.streamLevel == CustomLogger.WARNING
    assert CustomLogger.fileLevel == CustomLogger.DEBUG
    assert CustomLogger.isSaveLog == False
    assert CustomLogger.backupCount == 5
    assert CustomLogger.fileLogFmt == '%(asctime)s %(filename)s %(name)s '\
        '%(lineno)s %(levelname)s "%(message)s"'
    assert CustomLogger.streamLogFmt == '[%(levelname)s: File "%(filename)s", ' \
        'line %(lineno)s, in %(funcName)s] "%(message)s"'
    assert CustomLogger.dateFmt == '%Y-%m-%d %a %H:%M:%S'


def test_default_logger():  # {{{1
    logger = CustomLogger().logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'CustomLogger'
    assert len(logger.handlers) == 2

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.WARNING


def test_debugMode_self():  # {{{1
    logger_name = 'self debugMode test'
    clogger = CustomLogger(logger_name=logger_name)
    assert clogger.streamLevel == CustomLogger.WARNING

    clogger.debugMode()
    logger = clogger.logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert len(logger.handlers) == 1

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.DEBUG


def test_saveMode_self():  # {{{1
    logger_name = 'self saveMode test'
    CustomLogger.streamLevel = CustomLogger.WARNING
    clogger = CustomLogger(logger_name=logger_name)
    assert clogger.streamLevel == CustomLogger.WARNING

    clogger.isSaveLog = True
    logger = clogger.logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert len(logger.handlers) == 4

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.WARNING
    err_logger = logger.handlers[1]
    assert err_logger.level == CustomLogger.INFO
    err_logger = logger.handlers[2]
    assert err_logger.level == CustomLogger.DEBUG
    err_logger = logger.handlers[3]
    assert err_logger.level == CustomLogger.DEBUG


# END tests }}}1
