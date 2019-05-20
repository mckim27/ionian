#! /usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import datetime
from logzero import logger as log

class DynamoNewsMetaInfoStorer :

    __table = None

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.__table = dynamodb.Table('news_meta_info')


    def store_to_dynamo(self, news_info_list):
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
                        'parsing_flag': 0
                    }
                )

        log.info('### dynamo batch writer end :: news catecory - {0} - {1}, creating {2} obj success'.
                 format(news_info['category_name'], news_info['sub_category_name'], len(news_info_list)))