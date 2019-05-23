#! /usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import logging
import logzero
import os
from logzero import logger
from init.constant import DEV_ENV, STG_ENV, PROD_ENV, ERROR_ARG_EXIT_CODE, ERROR_LOAD_CONFIG_EXIT_CODE
from exception.custom_exception import *
from init import constant
from pathlib import Path


class ConfigLoader():

    def __init__(self, arg_env):
        if arg_env != DEV_ENV and arg_env != STG_ENV and arg_env != PROD_ENV:
            raise CannotRunException("arg_env is unknown... : {0}".format(arg_env), ERROR_ARG_EXIT_CODE)
        else:
            self.__CURRENT_ENV = arg_env
            logger.info("### Input ENV : {}".format(self.__CURRENT_ENV))

    def set_aws_info(self, aws_region, aws_access_key_id, aws_secret_access_key):
        home = str(Path.home())
        target_path = home + '/.aws'

        if aws_region is None or aws_access_key_id is None or aws_secret_access_key is None:
            logger.warn('### There is a empty value among aws_config inputs')
            logger.warn('### The dynamo_store feature is disabled ...')

            constant.CONFIG['aws_enable'] = False

        elif os.path.exists(target_path):
            logger.info('### aws_config exist ... config setting is passed. ')
            constant.CONFIG['aws_enable'] = True
        else:
            constant.CONFIG['aws_enable'] = True

            os.mkdir(target_path)
            with open(target_path + '/config', mode='wt', encoding='utf-8') as f:
                f.write(
                    '[default]\n' +
                    'region = ' + aws_region + '\n' +
                    'output = json\n')

            os.chmod(target_path + '/config', 0o600)

            with open(target_path + '/credentials', mode='wt', encoding='utf-8') as f:
                f.write(
                    '[default]\n' +
                    'aws_access_key_id = ' + aws_access_key_id + '\n' +
                    'aws_secret_access_key = ' + aws_secret_access_key + '\n')

            os.chmod(target_path + '/credentials', 0o600)

            logger.info('### aws_config setting is complete !!')

    def load_ionian_config(self) :
        load_file_path = './config/config_' + self.__CURRENT_ENV + ".yml"

        try:
            with open(load_file_path, 'r') as ymlfile:
                constant.CONFIG = yaml.safe_load(ymlfile)

            self.__set_logger()

            logger.info("### config loadFilePath : {}".format(load_file_path))
            logger.info("### CONFIG ###")
            logger.info(constant.CONFIG)

        except Exception as e:
            raise CannotRunException('loadConfig Exception : {}'.format(e), ERROR_LOAD_CONFIG_EXIT_CODE)

    def __set_logger(self):
        log_dir_fullpath = os.path.join(os.getcwd()) + '/' + constant.CONFIG['log_dir_name']
        log_file_fullpath = log_dir_fullpath + '/' + constant.CONFIG['log_file_name']

        if not os.path.exists(log_dir_fullpath):
            os.makedirs(log_dir_fullpath)

        logzero.logfile(log_file_fullpath, maxBytes=1000000, backupCount=7, encoding='utf8')

        logger.info('### logfile_full_path : {0}'.format(log_file_fullpath))
        logger.info('### log level : {0}'.format(constant.CONFIG['log_level']))

        if constant.CONFIG['log_level'].upper() == 'DEBUG'.upper():
            logzero.loglevel(level=logging.DEBUG)
        elif constant.CONFIG['log_level'].upper() == 'INFO'.upper():
            logzero.loglevel(level=logging.INFO)
        elif constant.CONFIG['log_level'].upper() == 'WARN'.upper():
            logzero.loglevel(level=logging.WARN)
        elif constant.CONFIG['log_level'].upper() == 'ERROR'.upper():
            logzero.loglevel(level=logging.ERROR)
        elif constant.CONFIG['log_level'].upper() == 'FATAL'.upper():
            logzero.loglevel(level=logging.FATAL)
        else:
            raise Exception('log_level setting Exception : Unknown log level :{}'.format(constant.CONFIG['log_level']))
