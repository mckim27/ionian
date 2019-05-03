#! /usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import logging
import logzero
import os
from logzero import logger
from config.constant import DEV_ENV, STG_ENV, PROD_ENV, ERROR_ARG_EXIT_CODE, ERROR_LOAD_CONFIG_EXIT_CODE
from exception.custom_exception import *

class ConfigLoader():

    def __init__(self, arg_env):
        if arg_env != DEV_ENV and arg_env != STG_ENV and arg_env != PROD_ENV:
            raise CannotRunException("arg_env is unknown... : {}".format(arg_env), ERROR_ARG_EXIT_CODE)
        else:
            self.__CURRENT_ENV = arg_env
            logger.info("### Input ENV : {}".format(self.__CURRENT_ENV))

            self.__CONFIG = None

    def load_config(self) :
        load_file_path = './config/config_' + self.__CURRENT_ENV + ".yml"

        try:
            with open(load_file_path, 'r') as ymlfile:
                self.__CONFIG = yaml.safe_load(ymlfile)

            self.__set_logger()

            logger.info("config loadFilePath : {}".format(load_file_path))

        except Exception as e:
            raise CannotRunException('loadConfig Exception : {}'.format(e), ERROR_LOAD_CONFIG_EXIT_CODE)

    def __set_logger(self):
        log_dir_fullpath = os.path.join(os.getcwd()) + '/' + self.__CONFIG['log_dir_name']
        log_file_fullpath = log_dir_fullpath + '/' + self.__CONFIG['log_file_name']

        if not os.path.exists(log_dir_fullpath):
            os.makedirs(log_dir_fullpath)

        logzero.logfile(log_file_fullpath, maxBytes=1000000, backupCount=7, encoding='utf8')

        if self.__CONFIG['log_level'].upper() == 'DEBUG'.upper():
            logzero.loglevel(level=logging.DEBUG)
        elif self.__CONFIG['log_level'].upper() == 'INFO'.upper():
            logzero.loglevel(level=logging.INFO)
        elif self.__CONFIG['log_level'].upper() == 'WARN'.upper():
            logzero.loglevel(level=logging.WARN)
        elif self.__CONFIG['log_level'].upper() == 'ERROR'.upper():
            logzero.loglevel(level=logging.ERROR)
        elif self.__CONFIG['log_level'].upper() == 'FATAL'.upper():
            logzero.loglevel(level=logging.FATAL)
        else:
            raise Exception('log_level setting Exception : Unknown log level :{}'.format(self.__CONFIG['log_level']))

