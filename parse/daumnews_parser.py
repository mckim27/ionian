#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from kafka import KafkaConsumer
import time
import json


class DaumNewsParser:

    # TODO config 에 kafka consumer option 추가 및 적용...
    __CONSUMER_TERM_SECONDS = 2

    def __init__(self):
        pass

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

                time.sleep(self.__CONSUMER_TERM_SECONDS)

        except KeyboardInterrupt:
            self.stop()

    # TODO html parse code 구현하기.
    def __parse(self):
        None