#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from collect.daumnews_collector import DaumNewsCollector
from parse.daumnews_parser import DaumNewsParser
from exception.custom_exception import CannotRunException
from init.constant import ERROR_NOT_IMPLEMENTATION


class CollectorFactory:

    @staticmethod
    def get_collector(target_site_name):
        if target_site_name == 'daum':
            log.info('### The {0} collector will be start as soon as ...'.format(target_site_name))

            return DaumNewsCollector()

        else:
            raise CannotRunException(
                '{0}-collector not implementation ...'.format(target_site_name),
                ERROR_NOT_IMPLEMENTATION)


class ParserFactory:

    @staticmethod
    def get_parser(target_site_name):
        if target_site_name == 'daum':
            log.info('### The {0} parser will be start as soon as ...'.format(target_site_name))

            return DaumNewsParser()
        else:
            raise CannotRunException(
                '{0}-parser not implementation ...'.format(target_site_name),
                ERROR_NOT_IMPLEMENTATION)
