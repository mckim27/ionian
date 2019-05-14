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

class DaumNewsParser:

    def stop(self):
        log.info('### Daum News Parser stopping ...')
        exit()

    def waiting_and_parsing(self):
        consumer = None

        try:
            while True:
                log.info('### Consumer is waiting ...')
                time.sleep(constant.CONFIG['consumer_waiting_term_seconds'])

                consumer = KafkaConsumer(
                    'news_meta_info', auto_offset_reset='latest',
                    bootstrap_servers=constant.CONFIG['kafka_brokers'], api_version=(0, 10),
                    consumer_timeout_ms=5000, max_poll_records=50
                )

                # TODO Parsing 된 text 저장하는 부분 구현
                for msg in consumer:
                    news_info = json.loads(msg.value)
                    # print(news_info)
                    self.parse(news_info)
                    log.info('### Parser sleeping ... wait a moment ... ')
                    time.sleep(constant.CONFIG['parser_waiting_term_seconds'])

                # auto commit default true
                consumer.close()
        except KeyboardInterrupt:
            self.stop()

        except Exception as e:
            raise ParserException('Occur to unexpected Exception in parser : {0}'.
                                  format(e), ERROR_UNEXPECTED_EXIT_CODE)

        finally:
            # 예상치 못하게 종료될 경우 현재 consumer close. 이미 close 되있다면 내부에서 알아서 그냥 리턴.
            if consumer is not None: consumer.close()

    # TODO html parse code 구현하기.
    def parse(self, news_info):
        log.debug('### parsing target url : {0}'.format(news_info['url']))

        result_text = None

        try:
            req = requests.get(news_info['url'])
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
                result_text += text_block.get_text()

        except Exception as e:
            log.error(get_pretty_traceback())

        finally:
            return result_text
