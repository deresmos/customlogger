import logging
import os
import shutil

from customlogger import CustomLogger


def pytest_report_header(config):
    return 'CustomLogger save log test'


def test_normal():
    clogger = CustomLogger(is_save_log=True)
    log_path = clogger._logDirPath

    # directory creation check
    assert os.path.isdir(log_path)

    # Number of log files check
    assert len(os.listdir(log_path)) == 2


def test_message():
    clogger = CustomLogger(is_save_log=True, logger_name='test2')
    log_path = clogger._logDirPath

    clogger.logger.debug('1')
    clogger.logger.info('2')
    clogger.logger.warning('3')
    clogger.logger.error('4')
    clogger.logger.critical('5')

    # directory creation check
    assert os.path.isdir(log_path)

    # Number of log files check
    assert len(os.listdir(log_path)) == 2

    # Number of log check
    with open(os.path.join(log_path, 'all.log')) as f:
        linenumber = len(f.readlines())

    assert linenumber == 5


def test_dirpath():
    log_path = 'logg'
    clogger = CustomLogger(
        is_save_log=True,
        logger_name='dir',
        log_dirpath=log_path,
    )
    assert log_path == clogger._logDirPath

    clogger.logger

    # directory creation check
    assert os.path.isdir(log_path)

    # Number of log files check
    assert len(os.listdir(log_path)) == 2


def test_cleanup():
    logs = ['log', 'logg']
    for logdir in logs:
        # Cleaning up
        if os.path.isdir(logdir):
            shutil.rmtree(logdir)
