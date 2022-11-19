import unittest
from threading import Thread

from nrt_logging.log_level import LogLevelEnum
from nrt_logging.logger import NrtLogger
from nrt_logging.logger_manager import logger_manager
from nrt_logging.logger_stream_handlers import \
    ConsoleStreamHandler, LogStyleEnum
from tests.test_nrt_logging.test_base import TestBase, NAME_1, stdout_redirect, r_stdout

A_MSG_1 = 'A METHOD 1'
A_MSG_2 = 'A METHOD 2'
A_MSG_3 = 'A METHOD 3'
B_MSG_1 = 'B METHOD 1'
C_MSG_1 = 'C METHOD 1'


class LoggerThread(Thread):
    __LOOP = 30

    __logger: NrtLogger

    def __init__(self):
        super().__init__()
        self.__logger = logger_manager.get_logger(NAME_1)

    def run(self):
        for _ in range(self.__LOOP):
            self.__a1()
            self.__a2()
            self.__a3()

    def __a1(self):
        self.__logger.info(A_MSG_1)
        self.__b()
        self.__logger.info(A_MSG_2)
        self.__logger.info(A_MSG_3)

    def __a2(self):
        self.__logger.info(A_MSG_1)
        self.__b()
        self.__logger.increase_depth()
        self.__logger.info(A_MSG_2)
        self.__logger.increase_depth()
        self.__logger.info(A_MSG_3)

    def __a3(self):
        self.__logger.info(A_MSG_1)
        self.__b()
        self.__logger.increase_depth()
        self.__logger.info(A_MSG_2)
        self.__logger.decrease_depth()
        self.__logger.info(A_MSG_3)

    def __b(self):
        self.__logger.info(B_MSG_1)
        self.__c()

    def __c(self):
        self.__logger.info(C_MSG_1)


class MultiThreadsTests(TestBase):
    def setUp(self):
        logger_manager.close_all_loggers()

    def tearDown(self):
        logger_manager.close_all_loggers()

    @stdout_redirect
    def test_01_multi_threads_not_crash(self):
        self.__create_logger_and_sh()
        multi_thread_list = []

        for _ in range(200):
            multi_thread_list.append(LoggerThread())

        for multi_thread in multi_thread_list:
            multi_thread.start()

        for multi_thread in multi_thread_list:
            multi_thread.join()

        so = r_stdout.getvalue()
        self.assertFalse('Exception' in so)

    @classmethod
    def __create_logger_and_sh(cls):
        sh = ConsoleStreamHandler()
        sh.style = LogStyleEnum.LINE
        sh.log_level = LogLevelEnum.TRACE
        logger = logger_manager.get_logger(NAME_1)
        logger.add_stream_handler(sh)
        return logger


if __name__ == '__main__':
    unittest.main()
