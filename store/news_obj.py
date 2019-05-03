#! /usr/bin/python
# -*- coding: utf-8 -*-


class NewsInfo:

    __title = None
    __press_name = None
    __link_url = None
    __publish_date = None

    def set_title(self, title):
        self.__title = title
        return self

    def set_press_name(self, press_name):
        self.__press_name = press_name
        return self

    def set_link_url(self, link_url):
        self.__link_url = link_url
        return self

    def set_publish_date(self, publish_date):
        self.__publish_date = publish_date
        return self
