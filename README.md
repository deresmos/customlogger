
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0fa228df20ff45a395382faa50fd34c2)](https://www.codacy.com/app/deresmos/customlogger?utm_source=github.com&utm_medium=referral&utm_content=deresmos/customlogger&utm_campaign=badger)

customlogger
==
Easy use logging.


Installation
--
* Install From PyPI
  ```
  pip install customlogger
  ```

* Install From source
  ```
  pip install .
  ```


Usage
--
* Standard usage
  ```python
  from customlogger import CustomLogger

  logger = CustomLogger().logger

  logger.debug('Debug message')
  logger.info('Info message')
  logger.warning('Warning message')
  logger.error('Error message')
  logger.critical('Critical message')
  ```

* Debug mode usage
  ```python
  from customlogger import CustomLogger

  # All logger of CustomLogger is debug mode.
  CustomLogger.debugMode()

  logger = CustomLogger().logger
  logger.debug('Debug message')
  logger.info('Info message')
  logger.warning('Warning message')
  logger.error('Error message')
  logger.critical('Critical message')
  ```

* Save log usage
  Save log in ./log dir
  ```python
  from customlogger import CustomLogger

  # All logger of CustomLogger save log file.
  # Default output log file path is './log/'
  CustomLogger.isSaveLog = True

  logger = CustomLogger().logger
  logger.debug('Debug message')
  logger.info('Info message')
  logger.warning('Warning message')
  logger.error('Error message')
  logger.critical('Critical message')
  ```

* SlackHandler usage
  ```python
  from customlogger import CustomLogger, SlackHandler

  custom_logger = CustomLogger()

  web_hooks = 'Your web hooks url'
  slack = SlackHandler(web_hooks)
  custom_logger.addHandler(slack, CustomLogger.INFO)

  logger = custom_logger.logger

  logger.debug('Debug message')
  logger.info('Info message')
  logger.warning('Warning message')
  logger.error('Error message')
  logger.critical('Critical message')
  ```


License
--
Released under the MIT license, see LICENSE.
