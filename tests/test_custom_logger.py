import logging

from customlogger import CustomLogger


def pytest_report_header(config):
    return 'custom_logger test'


def test_default_logger():  # {{{1
    logger = CustomLogger().logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'CustomLogger'
    assert len(logger.handlers) == 2

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.WARNING


def test_debug_self():  # {{{1
    logger_name = 'self debug test'
    clogger = CustomLogger(
        logger_name=logger_name, stream_level=CustomLogger.DEBUG)
    assert clogger.streamLevel == CustomLogger.DEBUG

    logger = clogger.logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert len(logger.handlers) == 1

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.DEBUG

    CustomLogger._STREAM_LEVEL = CustomLogger.WARNING


def test_saveMode_self():  # {{{1
    logger_name = 'self saveMode test'
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
