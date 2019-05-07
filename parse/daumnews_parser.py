#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import bs4
from logzero import logger as log
from kafka import KafkaConsumer
import requests
from bs4 import BeautifulSoup


class DaumNewsParser:

    # TODO config 에 kafka consumer option 추가 및 적용...
    __CONSUMER_WAITING_TERM_SECONDS = 2

    def stop(self):
        log.info('### Daum News Parser stopping ...')
        exit()

    def waiting_and_parsing(self):
        try:
            while True:
                consumer = KafkaConsumer(
                    'news_meta_info', auto_offset_reset='latest',
                    bootstrap_servers=['localhost:9092'], api_version=(0, 10),
                    consumer_timeout_ms=5000, max_poll_records=10
                )
                for msg in consumer:
                    news_info = json.loads(msg.value)
                    print(news_info)

                    # TODO parsing method 실행부.

                log.info('### Daum News Parser is waiting ...')

                time.sleep(self.__CONSUMER_WAITING_TERM_SECONDS)

        except KeyboardInterrupt:
            self.stop()

    # TODO html parse code 구현하기.
    def parse(self, news_info):
        log.debug('### parsing target url : {0}'.format(news_info['url']))

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
        text = text_container.find('section')
        log.debug(text)

