#! /usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Crawler(ABC) :

    @abstractmethod
    def waiting_and_crawling(self):
        pass

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def stop(self):
        pass