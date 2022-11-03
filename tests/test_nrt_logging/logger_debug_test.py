import unittest

import yaml

from nrt_logging.log_format import LogDateFormat, LogElementEnum
from nrt_logging.log_level import LogLevelEnum
from nrt_logging.logger_manager import logger_manager
from nrt_logging.logger_stream_handlers import \
    ConsoleStreamHandler, LogStyleEnum, ManualDepthEnum
from tests.test_nrt_logging.test_base import \
    NAME_1, stdout_redirect, r_stdout, TestBase


TEST_FILE_NAME = 'logger_debug_test.py'


class LoggersDebugTests(TestBase):

    # skipcq: PYL-R0201
    def setUp(self):
        logger_1 = logger_manager.get_logger(NAME_1)

        if logger_1:
            logger_1.close_stream_handlers()

    # skipcq: PYL-R0201
    def tearDown(self):
        logger_manager.is_debug = False

    @stdout_redirect
    def test_debug_in_logger_manager_with_line_style(self):
        logger_manager.is_debug = True
        sh = ConsoleStreamHandler()
        sh.style = LogStyleEnum.LINE
        sh.log_level = LogLevelEnum.TRACE
        logger = logger_manager.get_logger(NAME_1)
        logger.add_stream_handler(sh)
        msg_1 = 'abc'
        child_1 = 'child'
        method_name = 'test_debug_in_logger_manager_with_line_style'
        logger.trace(msg_1)
        logger.info(child_1, manual_depth=ManualDepthEnum.INCREASE)
        so = r_stdout.getvalue()
        log_list = yaml.safe_load(so)
        self.assertEqual(len(log_list), 1)

        log_line = log_list[0]['log']

        self._verify_log_line(
            log_line,
            LogDateFormat.DEFAULT_DATE_FORMAT,
            LogLevelEnum.TRACE,
            f'{TEST_FILE_NAME}.{self.__class__.__name__}',
            method_name,
            41,
            msg_1,
            True)

        children = log_list[0].get('children')
        self.assertIsNotNone(children)
        self.assertEqual(1, len(children))

        self._verify_log_line(
            children[0]['log'],
            LogDateFormat.DEFAULT_DATE_FORMAT,
            LogLevelEnum.INFO,
            f'{TEST_FILE_NAME}.{self.__class__.__name__}',
            method_name,
            42,
            child_1,
            True)

    @stdout_redirect
    def test_debug_in_logger_with_yaml_style(self):
        sh = ConsoleStreamHandler()
        sh.style = LogStyleEnum.YAML
        sh.log_level = LogLevelEnum.TRACE
        logger = logger_manager.get_logger(NAME_1)
        logger.is_debug = True
        logger.add_stream_handler(sh)
        msg = 'abc'
        logger.trace(msg)
        so = r_stdout.getvalue()
        log_doc = yaml.safe_load(so)
        self.assertTrue(log_doc)
        self.assertEqual(
            LogLevelEnum.TRACE.name,
            log_doc.get(LogElementEnum.LOG_LEVEL.element_name))
        message = log_doc.get(LogElementEnum.MESSAGE.element_name)
        self.assertIsNotNone(message)
        self.assertTrue(message.startswith(f'{msg}\nNRT-Logging DEBUG:'))

    @stdout_redirect
    def test_debug_in_stream_handler_with_yaml_style(self):
        sh = ConsoleStreamHandler()
        sh.style = LogStyleEnum.YAML
        sh.log_level = LogLevelEnum.INFO
        sh.is_debug = True
        logger = logger_manager.get_logger(NAME_1)
        logger.add_stream_handler(sh)
        msg = 'test123'
        logger.info(msg)
        so = r_stdout.getvalue()
        log_doc = yaml.safe_load(so)
        self.assertTrue(log_doc)
        self.assertEqual(
            LogLevelEnum.INFO.name,
            log_doc.get(LogElementEnum.LOG_LEVEL.element_name))
        message = log_doc.get(LogElementEnum.MESSAGE.element_name)
        self.assertIsNotNone(message)
        self.assertTrue(message.startswith(f'{msg}\nNRT-Logging DEBUG:'))


if __name__ == '__main__':
    unittest.main()
