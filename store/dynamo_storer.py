#! /usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import datetime
from logzero import logger as log
from init import constant


class DynamoNewsMetaInfoStorer :

    __table = None

    def __init__(self):
        if constant.CONFIG['aws_enable']:
            dynamodb = boto3.resource('dynamodb')
            self.__table = dynamodb.Table('news_meta_info')
        else:
            log.warn('### You can not use the dynamo store feature ....')
            
    def store(self, news_info_list, site_name):

        if self.__table is None:
            log.warn('### nothing to do ...')
            return

        # 뉴스 갯수가 많으므로 batch writer 이용.
        with self.__table.batch_writer() as batch:
            for news_info in news_info_list:
                batch.put_item(
                    Item={
                        'origin_create_date': news_info['origin_create_date'],
                        'url': news_info['url'],
                        'title': news_info['title'],
                        'press_name': news_info['press_name'],
                        'category_name' : news_info['category_name'],
                        'category_en_name': news_info['category_en_name'],
                        'sub_category_name': news_info['sub_category_name'],
                        'sub_category_en_name': news_info['sub_category_en_name'],
                        'create_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
                        'site_name' : site_name
                    }
                )

        log.info('### dynamo batch writer end :: creating {0} obj success'.format(len(news_info_list)))