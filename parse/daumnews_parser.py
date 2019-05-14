#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
from logzero import logger as log
from kafka import KafkaConsumer
import requests
from bs4 import BeautifulSoup
from init import constant


class DaumNewsParser:

    def stop(self):
        log.info('### Daum News Parser stopping ...')
        exit()

    def waiting_and_parsing(self):
        try:
            while True:
                consumer = KafkaConsumer(
                    'news_meta_info', auto_offset_reset='latest',
                    bootstrap_servers=constant.CONFIG['kafka_brokers'], api_version=(0, 10),
                    consumer_timeout_ms=5000, max_poll_records=20
                )

                for msg in consumer:
                    news_info = json.loads(msg.value)
                    # print(news_info)
                    self.parse(news_info)
                    log.info('### Parser sleeping ... wait a moment ... ')
                    time.sleep(constant.CONFIG['parser_waiting_term_seconds'])

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
        # text = text_container.find_all('section')
        re = text_container.find_all("p", attrs={"dmcf-ptype":True})
        for text_block in re:
            log.debug(text_block.get_text())


