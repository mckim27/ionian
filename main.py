#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import traceback
from coverage import __version__
from exception.custom_exception import *
from logzero import logger as log
from init.config_loader import ConfigLoader
from init.constant import *
from utils.etc import get_pretty_traceback
from init.factory import CollectorFactory, CrawlerFactory

if __name__ == "__main__" :
    try:
        parser = argparse.ArgumentParser(description='news crawler.')
        parser.add_argument('--target', type=str, nargs='?', default='daum',
                            help='input target news site. now only DAUM site is supported...')

        parser.add_argument('--role', type=str, nargs='?', default='collector',
                            help='input some role. \'collector\' or \'crawler\'')

        parser.add_argument('--env', type=str, nargs='?', default='dev',
                            help='input run env. \'dev\' or \'stg\' or \'prd\'')

        parser.add_argument('--aws_region', type=str, nargs='?', default='',
                            help='aws-config region info. not requirement.')

        parser.add_argument('--aws_access_key_id', type=str, nargs='?', default='',
                            help='aws_access_key_id info. not requirement.')

        parser.add_argument('--aws_secret_access_key', type=str, nargs='?', default='',
                            help='aws_secret_access_key info. not requirement.')

        args = parser.parse_args()
        target_site = args.target.lower()
        role = args.role.lower()
        arg_env = args.env.lower()

        aws_region = args.aws_region
        aws_access_key_id = args.aws_access_key_id
        aws_secret_access_key = args.aws_secret_access_key

        config_loader = ConfigLoader(arg_env)

        config_loader.load_ionian_config()

        log.info('### Ionian News Crawler v{0}'.format(__version__))

        config_loader.set_aws_info(aws_region, aws_access_key_id, aws_secret_access_key)

        log.info('### input arg_env : {0}'.format(arg_env))
        log.info('### input role : {0}'.format(role))
        log.info('### input target_site : {0}'.format(target_site))

        if role == 'collector' :
            collector = CollectorFactory.get_collector(target_site)
            collector.collect()

        else:
            parser = CrawlerFactory.get_crawler(target_site)
            parser.waiting_and_crawling()

    except CannotRunException as cre:
        log.error(traceback.format_exc())
        cre.exit()

    except CollectorException as ce:
        log.error(traceback.format_exc())
        ce.exit()

    except Exception as e:
        log.error('Main Error Unexpected Exception... e : {0}'.format(traceback.format_exc()))
        exit(ERROR_UNEXPECTED_EXIT_CODE)





