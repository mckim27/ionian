#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from logzero import logger as log
from utils.text_util import assert_str_and_empty, assert_str_and_length
from init import constant
'''
new_info dict
    'origin_create_date': 'yyyyMMddHHmmssSSS'
    'url': 'xxx',
    'title': 'xxx',
    'press_name': 'xxx',
    'category_name' : 'xxx',
    'category_en_name': 'xxx',
    'sub_category_name': 'xxx',
    'sub_category_en_name': 'xxx'
    'contents': 'xxxxxxxxxxxxxx'
'''


class DaumNewsTextFileStorer:
    # text/news/daum/{yyyy-mm-dd}/{main_cate}/{subcate}/{origin_create_date}

    def __init__(self):
        self.__text_store_path = constant.CONFIG['data_root_path'] + '/news/daum'

        if not os.path.exists(self.__text_store_path):
            data_path = Path(self.__text_store_path)
            data_path.mkdir(parents=True, exist_ok=False)
            log.info('### data root path create success. data_root_path : {0}'.format(self.__text_store_path))

    def store(self, news_info):
        assert_str_and_length(news_info['origin_create_date'], 17)

        ymd_date = news_info['origin_create_date']
        ymd_date = ymd_date[:8]
        store_path = self.__text_store_path + '/' + ymd_date

        if not os.path.exists(store_path):
            os.mkdir(store_path)

        # assert category_en_name
        assert_str_and_empty(news_info['category_en_name'])

        store_path += '/' + news_info['category_en_name']
        if not os.path.exists(store_path):
            os.mkdir(store_path)

        # assert sub_category_en_name
        assert_str_and_empty(news_info['sub_category_en_name'])

        if news_info['sub_category_en_name'] != '-':
            store_path += '/' + news_info['sub_category_en_name']
            if not os.path.exists(store_path):
                os.mkdir(store_path)

        # TODO news contents 빈값인 경우의 처리.

        store_path += '/' + news_info['origin_create_date'] + '.html'

        # 파일 이름이 이미 존재하면 저장하지 않고 false return
        if os.path.exists(store_path):
            log.warn('### file "{0}" exist ... '.format(store_path))

            return False
        else:
            with open(store_path, mode='wt', encoding='utf-8') as f:
                f.write(news_info['contents'])

            log.info('### file "{0}" create success.'.format(store_path))

            return True
