#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import time
from logzero import logger as log
from utils.date_util import get_previous_day
from bs4 import BeautifulSoup
from collect.collector import Collector
from exception.custom_exception import CollectorException
from config.constant import ERROR_UNEXPECTED_EXIT_CODE


class DaumNewsCollector(Collector):

    def __init__(self):
        self.BASE_URL = 'https://media.daum.net'
        self.PAGE_PARAM_KEY = 'page='
        self.DATE_PARAM_KEY = 'regDate='
        self.TARGET_DATE = get_previous_day(1, "%Y%m%d")

        # 2019-05-02 기준 daum news category.
        # 각 category 에 따라 api path 마지막이 결정됨. 컬럼과 보도자료는 사용 안함.
        self.MAIN_CATE_TAIL_PATH = [
            'breakingnews/society',
            'breakingnews/politics',
            'breakingnews/economic',
            'breakingnews/foreign',
            'breakingnews/culture',
            'breakingnews/entertain',
            'breakingnews/sports',
            'breakingnews/digital'
        ]

    # override.
    def collect(self):
        try:
            for tail_path in self.MAIN_CATE_TAIL_PATH:
                target_url = self.BASE_URL + '/' + tail_path

                sub_cate_urls = self.__get_sub_categories(target_url)

                # 하위 카테고리 없는 경우의 처리.
                if len(sub_cate_urls) is 0:
                    sub_cate_urls.append(target_url)

                log.debug('### sub_cate_urls ###')
                log.debug('\n'.join(sub_cate_urls))

                for sub_cate_url in sub_cate_urls:
                    req_page = 1

                    log.debug('### sub_cate_url : {0}'.format(sub_cate_url))

                    while self.__is_exist_page(sub_cate_url, req_page, self.TARGET_DATE):
                        if req_page is 2 :
                            break

                        log.debug('waiting...')
                        time.sleep(2)

                        self.__get_newslist(sub_cate_url, req_page, self.TARGET_DATE)
                        req_page += 1

                # TODO 추후 break 삭제
                break
        except Exception as e:
            raise CollectorException('Collector Exception : {}'.format(e), ERROR_UNEXPECTED_EXIT_CODE)

    def store(self):
        None

    def __get_sub_categories(self, cate_url):
        req = requests.get(cate_url)
        html = req.text

        header = req.headers
        status = req.status_code
        is_ok = req.ok

        soup = BeautifulSoup(html, 'html.parser')

        sub_cate_els = soup.find('ul', class_='tab_sub2')

        sub_cate_urlpaths = []

        # print('cate_url : ', cate_url)

        if sub_cate_els is not None:
            for el in sub_cate_els:
                if type(el) is not bs4.element.NavigableString:
                    sub_cate_tailpath = el.find('a', class_='link_txt').get('href')

                    if cate_url != self.BASE_URL + sub_cate_tailpath:
                        sub_cate_urlpaths.append(self.BASE_URL + sub_cate_tailpath)

        return sub_cate_urlpaths

    def __get_newslist(self, target_url, req_page, reg_date):
        # ex) https://media.daum.net/breakingnews/society/affair?page=1&regDate=20190501
        # TODO news Object 만들어서 list 로 만들고 return 하도록 구현예정.
        target_url += '?' + self.PAGE_PARAM_KEY + str(req_page) + '&' + self.DATE_PARAM_KEY + reg_date
        log.debug('target_url : {0}'.format(target_url))
        req = requests.get(target_url)
        html = req.text

        header = req.headers
        status = req.status_code
        is_ok = req.ok

        soup = BeautifulSoup(html, 'html.parser')

        # target : ul class list_news2 list_allnews
        news_list_obj = soup.find('ul', class_='list_allnews')
        for el in news_list_obj:
            if type(el) is not bs4.element.NavigableString:
                # print(el)

                new_title = el.find('a', class_='link_txt').get_text()
                log.debug(new_title)

                news_url = el.find('a', class_='link_txt').get('href')
                log.debug(news_url)

                news_info = el.find('span', class_='info_news').get_text().replace(' ', '').split('·')

                press_name = news_info[0]
                log.debug(press_name)

                publish_time = news_info[1]
                log.debug(publish_time)

    def __is_exist_page(self, target_url, req_page, reg_date):
        target_url += '?' + self.PAGE_PARAM_KEY + str(req_page) + '&' + self.DATE_PARAM_KEY + reg_date
        req = requests.get(target_url)
        is_ok = req.ok
        return is_ok
