#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

from abc import ABC, abstractmethod
from store.kafka_producer import IonianKafkaProducer


class Collector(ABC) :

    # kafka lib 변경될 수도 있으니 일단 producer 자체는 여기서 가지고 있도록 함.
    def __init__(self):
        self.__producer = IonianKafkaProducer()

    def publish_message(self, topic_name, key, msg_dict):
        self.__producer.publish_message(topic_name, key, json.dumps(msg_dict))

    def close(self):
        self.__producer.close()

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def store(self):
        pass