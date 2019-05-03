#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import traceback
from exception.custom_exception import *
from logzero import logger as log
from collect.daumnews_collector import DaumNewsCollector
from config.config_loader import ConfigLoader
from config.constant import *


if __name__ == "__main__" :
    try:
        parser = argparse.ArgumentParser(description='news crawler.')
        parser.add_argument('--target', type=str, nargs='?', default='daum',
                            help='input target news site. now only DAUM site is supported...')

        parser.add_argument('--role', type=str, nargs='?', default='collector',
                            help='input some role. \'collector\' or \'parser\'')

        parser.add_argument('--env', type=str, nargs='?', default='dev',
                            help='input run env. \'dev\' or \'stg\' or \'prd\'')

        args = parser.parse_args()
        target_site = args.target.upper()
        role = args.role.lower()
        arg_env = args.env.lower()

        config_loader = ConfigLoader(arg_env)

        config_loader.load_config()

        if role == 'collector' :
            if target_site == 'DAUM':
                log.info('### collector start. target site : {0}'.format(target_site))

                collector = DaumNewsCollector()
                collector.collect()
            else:
                log.info('### input target site : {0}'.format(target_site))
                log.info('{0}-collector not implemented...'.format(target_site))
        else:
            if target_site == 'DAUM':
                log.info('### parser start. target site : {0}'.format(target_site))
                log.info('not implemented...')
            else:
                log.info('### input target site : {0}'.format(target_site))
                log.info('{0}-parser not implemented...'.format(target_site))

    except CannotRunException as cre:
        log.error(traceback.format_exc())
        cre.exit()

    except CollectorException as ce:
        log.error(traceback.format_exc())
        ce.exit()

    except Exception as e:
        log.error('Main Error Unknown Exception... e : {}'.format(traceback.format_exc()))
        exit(ERROR_UNEXPECTED_EXIT_CODE)





