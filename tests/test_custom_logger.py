import logging

from customlogger import CustomLogger


def pytest_report_header(config):
    return 'custom_logger test'


def test_default_params():  # {{{1
    assert CustomLogger._ALL_LOG_FILENAME == 'all.log'
    assert CustomLogger._LOG_DIRPATH == './log'
    assert CustomLogger._STREAM_LEVEL == CustomLogger.WARNING
    assert CustomLogger._FILE_LEVEL == CustomLogger.DEBUG
    assert CustomLogger.isSaveLog is False
    assert CustomLogger.isColorLog is True
    assert CustomLogger._BACKUP_COUNT == 5


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
    assert clogger.stream_level == CustomLogger.DEBUG

    logger = clogger.logger
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert len(logger.handlers) == 1

    err_logger = logger.handlers[0]
    assert err_logger.level == CustomLogger.DEBUG

    CustomLogger._STREAM_LEVEL = CustomLogger.WARNING


def test_saveMode_self():  # {{{1
    logger_name = 'self saveMode test'
    CustomLogger.stream_level = CustomLogger.WARNING
    clogger = CustomLogger(logger_name=logger_name)
    assert clogger.stream_level == CustomLogger.WARNING

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
