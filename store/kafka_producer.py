#! /usr/bin/python
# -*- coding: utf-8 -*-

from kafka import KafkaProducer
from logzero import logger as log
from config import constant


class IonianKafkaProducer:

    __producer = None

    def __init__(self):
        try:
            print(constant.CONFIG['kafka_brokers'])
            self.__producer = KafkaProducer(
                bootstrap_servers=constant.CONFIG['kafka_brokers'], api_version=(0, 10))
        except Exception as ex:
            log.error('Exception while connecting Kafka')
            raise ex

    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.__producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.__producer.flush()
        except Exception as ex:
            log.error('Exception in publishing message')
            raise ex

    def close(self):
        if self.__producer is not None:
            self.__producer.close()