#! /usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import datetime
from logzero import logger as log

class Storer :

    __store_type = None

    def __init__(self, store_type='dynamo'):
        __store_type = store_type


    def store_to_dynamo(self, news_info_list, cate_name=None):
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('news_meta_info')

        # 뉴스 갯수가 많으므로 batch writer 이용.
        with table.batch_writer() as batch:
            for news_info in news_info_list:
                batch.put_item(
                    Item={
                        'origin_create_date': news_info['origin_create_date'],
                        'url': news_info['url'],
                        'title': news_info['title'],
                        'press_name': news_info['press_name'],
                        'create_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    }
                )

        if cate_name is not None:
            log.info('### dynamo batch writer end :: news catecory - {0} creating success'.format(cate_name))