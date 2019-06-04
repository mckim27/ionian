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
from init.constant import ERROR_UNEXPECTED_EXIT_CODE
from init import constant


class DaumNewsCollector(Collector):

    def __init__(self):
        Collector.__init__(self)

        self.SITE_NAME = 'daum'
        self.BASE_URL = 'https://media.daum.net'
        self.PAGE_PARAM_KEY = 'page='
        self.DATE_PARAM_KEY = 'regDate='
        self.TARGET_DATE = get_previous_day(1, "%Y%m%d")

        # 2019-05-02 기준 daum news category.
        # 각 category 에 따라 api path 마지막이 결정됨. 컬럼과 보도자료는 사용 안함.
        self.MAIN_CATE_INFO = [
            {
                'category_name' : '사회',
                'category_en_name': 'society',
                'url_tail_path' : 'breakingnews/society'
            },
            {
                'category_name': '정치',
                'category_en_name': 'politics',
                'url_tail_path': 'breakingnews/politics'
            },
            {
                'category_name': '경제',
                'category_en_name': 'economic',
                'url_tail_path': 'breakingnews/economic'
            },
            {
                'category_name': '국제',
                'category_en_name': 'foreign',
                'url_tail_path': 'breakingnews/foreign'
            },
            {
                'category_name': '문화',
                'category_en_name': 'culture',
                'url_tail_path': 'breakingnews/culture'
            },
            {
                'category_name': '연예',
                'category_en_name': 'entertain',
                'url_tail_path': 'breakingnews/entertain'
            },
            {
                'category_name': '스포츠',
                'category_en_name': 'sports',
                'url_tail_path': 'breakingnews/sports'
            },
            {
                'category_name': 'IT',
                'category_en_name': 'digital',
                'url_tail_path': 'breakingnews/digital'
            }
        ]

        self.__new_count = 0

    # override.
    def collect(self):
        try:
            # main category loop start.
            for cate_info in self.MAIN_CATE_INFO:
                target_url = self.BASE_URL + '/' + cate_info['url_tail_path']

                sub_cate_info_list = self.__get_sub_categories(target_url)

                # 하위 카테고리 없는 경우의 처리.
                if len(sub_cate_info_list) is 0:
                    sub_cate_info_list.append({
                        'url' : target_url,
                        'sub_category_name': '-',
                        'sub_category_en_name': '-'
                    })

                log.debug('### sub_cate_urls ###')
                log.debug(sub_cate_info_list)

                # sub category loop start
                for sub_cate_info in sub_cate_info_list:
                    req_page = 1

                    log.debug('### sub_cate_url : {0}'.format(sub_cate_info['url']))

                    while self.__is_exist_page(sub_cate_info['url'], req_page, self.TARGET_DATE):
                        log.debug('### collector is waiting ...')
                        time.sleep(constant.CONFIG['collector_waiting_term_seconds'])

                        news_list = self.__get_newslist(
                            cate_info, sub_cate_info, req_page, self.TARGET_DATE)

                        # 빈값이라면 마지막 페이지...
                        if len(news_list) is 0 :
                            break

                        for news in news_list:
                            self.publish_message(
                                constant.CONFIG['news_topic_name'],
                                news['origin_create_date'],
                                news
                            )

                        self.__new_count += len(news_list)
                        req_page += 1
                # sub category loop end
            # main category loop end.

            # producer close.
            self.close()

            log.info('The daum news collector\'s job is finished. total news count : {0}'.format(self.__new_count))

        except Exception as e:
            raise CollectorException('Occur to unexpected Exception in collector : {0}'.
                                     format(e), ERROR_UNEXPECTED_EXIT_CODE)

    def __get_sub_categories(self, cate_url):
        req = requests.get(cate_url)
        html = req.text

        header = req.headers
        status = req.status_code
        is_ok = req.ok

        if not is_ok:
            raise Exception('request Exception...')

        print(cate_url)

        soup = BeautifulSoup(html, 'html.parser')

        sub_cate_els = soup.find('ul', class_='tab_sub2')

        sub_cate_info_list = []

        # sub category 가 없을수도 있음.
        if sub_cate_els is not None:
            for el in sub_cate_els:
                if type(el) is not bs4.element.NavigableString:
                    sub_cate_tailpath = el.find('a', class_='link_txt').get('href')

                    # 전체 기사 항목 건너뜀.
                    if cate_url != self.BASE_URL + sub_cate_tailpath:
                        sub_cate_info = {}

                        sub_cate_name = el.find('a', class_='link_txt').get_text()
                        sub_cate_info['url'] = self.BASE_URL + sub_cate_tailpath
                        sub_cate_info['sub_category_name'] = sub_cate_name
                        sub_cate_info['sub_category_en_name'] = sub_cate_tailpath[sub_cate_tailpath.rfind('/') + 1:]
                        sub_cate_info_list.append(sub_cate_info)

        return sub_cate_info_list

    def __get_newslist(self, cate_info, sub_cate_info, req_page, reg_date):
        # ex) https://media.daum.net/breakingnews/society/affair?page=1&regDate=20190501

        target_url = sub_cate_info['url']
        target_url += '?' + self.PAGE_PARAM_KEY + str(req_page) + '&' + self.DATE_PARAM_KEY + reg_date
        log.debug('target_url : {0}'.format(target_url))
        req = requests.get(target_url)
        html = req.text

        header = req.headers
        status = req.status_code
        is_ok = req.ok

        if not is_ok :
            raise Exception('request Exception....')

        soup = BeautifulSoup(html, 'html.parser')

        # target : ul class list_news2 list_allnews
        news_list_obj = soup.find('ul', class_='list_allnews')

        news_info_list = []

        # 마지막 페이지일 경우 빈값 리턴.
        if type(news_list_obj) is type(None):
            return news_info_list

        for el in news_list_obj:

            if type(el) is not bs4.element.NavigableString:
                # print(el)
                news_info = {}
                news_info['site_name'] = self.SITE_NAME
                news_info['category_name'] = cate_info['category_name']
                news_info['category_en_name'] = cate_info['category_en_name']
                news_info['sub_category_name'] = sub_cate_info['sub_category_name']
                news_info['sub_category_en_name'] = sub_cate_info['sub_category_en_name']

                new_title = el.find('a', class_='link_txt').get_text()
                log.debug(new_title)
                news_info['title'] = new_title

                news_url = el.find('a', class_='link_txt').get('href')
                log.debug(news_url)
                news_info['url'] = news_url

                news_info_el = el.find('span', class_='info_news').get_text().replace(' ', '').split('·')

                press_name = news_info_el[0]
                # log.debug(press_name)
                news_info['press_name'] = press_name

                origin_create_date = news_url[news_url.rfind('/') + 1:]
                # log.debug(origin_create_date)
                news_info['origin_create_date'] = origin_create_date

                news_info_list.append(news_info)

        return news_info_list

    def __is_exist_page(self, target_url, req_page, reg_date):
        target_url += '?' + self.PAGE_PARAM_KEY + str(req_page) + '&' + self.DATE_PARAM_KEY + reg_date
        req = requests.get(target_url)
        is_ok = req.ok
        return is_ok
