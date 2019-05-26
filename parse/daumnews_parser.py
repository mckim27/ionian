#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
from logzero import logger as log
from kafka import KafkaConsumer
import requests
from bs4 import BeautifulSoup
from init import constant
from exception.custom_exception import ParserException
from init.constant import ERROR_UNEXPECTED_EXIT_CODE
from utils.etc import get_pretty_traceback
from store.news_textfile_storer import DaumNewsTextFileStorer
from store.dynamo_storer import DynamoNewsMetaInfoStorer
from sys import exit
from parse.parser import Parser
from utils.text_util import is_empty_text, is_short_text, assert_str_default


class DaumNewsParser(Parser):

    def __init__(self):
        self.__text_storer = DaumNewsTextFileStorer()
        self.__meta_info_storer = DynamoNewsMetaInfoStorer()

    # override
    def stop(self):
        log.info('### Daum News Parser stopping ...')
        exit()

    # text data validation 필요함.
    #  영어기사도 존재. 빈 텍스트도 존재.
    #  한글이라도 글자수가 너무 적을 경우는 저장하지 않도록 변경 필요.
    def __is_validate_text(self, text):
        assert_str_default(text)

        return not is_empty_text(text) and not is_short_text(text)

    # override
    def waiting_and_parsing(self):
        # consumer 연결 한번으로 변경.
        consumer = KafkaConsumer(
            constant.CONFIG['daum_news_topic_name'],
            auto_offset_reset='latest', group_id='daum_news',
            bootstrap_servers=constant.CONFIG['kafka_brokers'], api_version=(0, 10),
            consumer_timeout_ms=5000, max_poll_records=10
        )

        try:
            while True:
                log.info('### Consumer is waiting ...')
                time.sleep(constant.CONFIG['consumer_waiting_term_seconds'])

                news_meta_info_list = []

                item_count = 0
                for msg in consumer:
                    news_info = json.loads(msg.value)

                    # print(news_info)
                    news_contents = self.parse(news_info['url'])

                    news_info['contents'] = news_contents

                    # 유효한 텍스트, 저장이 성공적으로 되었을 경우만 DB 에 저장할 list 에 append 함.
                    if self.__is_validate_text(news_info['contents']) and \
                            self.__text_storer.store(news_info):
                        news_meta_info_list.append(news_info)
                        item_count += 1

                    # 특정 갯수가 되면 dynamo db 에 insert
                    if item_count >= constant.CONFIG['db_writer_size']:
                        self.__meta_info_storer.store(news_meta_info_list, 'daum')
                        news_meta_info_list = []
                        item_count = 0
                    else:
                        log.debug('### item_count : {0}'.format(item_count))

                if len(news_meta_info_list) != 0:
                    self.__meta_info_storer.store(news_meta_info_list, 'daum')

        except KeyboardInterrupt:
            # stop 으로 exit 호출되어도 sys.exit 이기에 finally 동작.
            self.stop()

        except Exception as e:
            raise ParserException('Occur to unexpected Exception in parser : {0}'.
                                  format(e), ERROR_UNEXPECTED_EXIT_CODE)

        finally:
            # 종료될 경우 현재 consumer close. 이미 close 되있다면 내부에서 알아서 그냥 리턴.
            if consumer is not None:
                consumer.close()

    # override
    def parse(self, page_url):
        log.debug('### parsing target url : {0}'.format(page_url))

        result_text = ''

        try:
            log.info('### Parser waiting ... wait a moment ... ')
            time.sleep(constant.CONFIG['parser_waiting_term_seconds'])

            req = requests.get(page_url)
            html = req.text

            header = req.headers
            status = req.status_code
            is_ok = req.ok

            if not is_ok:
                raise Exception('request Exception...')

            soup = BeautifulSoup(html, 'html.parser')
            news_view = soup.find('div', class_='news_view')
            # log.debug(news_view)

            # TODO summary_view 있는 경우 있음.

            text_container = news_view.find('div', id='harmonyContainer')
            # text = text_container.find_all('section')
            re = text_container.find_all("p", attrs={"dmcf-ptype":True})

            for text_block in re:
                log.debug(text_block.get_text())

                if result_text != '':
                    result_text += '\n'

                result_text += text_block.get_text()

        except Exception as e:
            log.error(get_pretty_traceback())

        finally:
            return result_text
