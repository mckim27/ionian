# -*- coding: utf-8 -*-
import requests
import bs4
from utils.date_util import get_previous_day
from bs4 import BeautifulSoup

BASE_URL = 'https://media.daum.net'
PAGE_PARAM_KEY = 'page='
DATE_PARAM_KEY = 'regDate='
TARGET_DATE = get_previous_day(1, "%Y%m%d")

def collect():
    # 2019-05-02 기준 daum news category.
    # 각 category 에 따라 api path 마지막이 결정됨. 컬럼과 보도자료는 사용 안함.
    category_root_tailpaths = [
        'breakingnews/society',
        'breakingnews/politics',
        'breakingnews/economic',
        'breakingnews/foreign',
        'breakingnews/culture',
        'breakingnews/entertain',
        'breakingnews/sports',
        'breakingnews/digital'
    ]

    for tailpath in category_root_tailpaths:
        target_url = BASE_URL + '/' + tailpath

        sub_cate_urls = get_sub_categorys(target_url)

        if len(sub_cate_urls) is not 0 :
            print("\n".join(sub_cate_urls))

        for sub_cate_url in sub_cate_urls :
            req_page = 1

            while(isExistPage(sub_cate_url, req_page, TARGET_DATE)) :
                # if start_page is 5 : break
                get_newslist(sub_cate_url, req_page, TARGET_DATE)
                req_page += 1

        # TODO 추후 break 삭제
        break

def get_sub_categorys (target_url) :
    req = requests.get(target_url)
    html = req.text

    header = req.headers
    status = req.status_code
    is_ok = req.ok

    soup = BeautifulSoup(html, 'html.parser')

    sub_cate_els = soup.find('ul', class_='tab_sub2')

    sub_cate_urlpaths = []

    if sub_cate_els != None:
        print('target_url : ', target_url)
        for el in sub_cate_els:
            if type(el) is not bs4.element.NavigableString:
                sub_cate_tailpath = el.find('a', class_='link_txt').get('href')

                if target_url != BASE_URL + sub_cate_tailpath :
                    sub_cate_urlpaths.append(BASE_URL + sub_cate_tailpath)

                    # TODO 추후 break 삭제
                    break

    return sub_cate_urlpaths

def get_newslist (target_url, req_page, reg_date):
    # ex) https://media.daum.net/breakingnews/society/affair?page=1&regDate=20190501
    start_page = 1
    # TODO news Object 만들어서 list 로 만들고 return 하도록 구현예정.
    target_url += '?' + PAGE_PARAM_KEY + str(req_page) + '&' + DATE_PARAM_KEY + reg_date
    print('extract_urls target_url : ', target_url)
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
            print(new_title)

            news_url = el.find('a', class_='link_txt').get('href')
            print(news_url)

            news_info = el.find('span', class_='info_news').get_text().replace(' ', '').split('·')

            press_name = news_info[0]
            print(press_name)

            publish_time = news_info[1]
            print(publish_time)

def isExistPage(target_url, req_page, reg_date):
    target_url += '?' + PAGE_PARAM_KEY + str(req_page) + '&' + DATE_PARAM_KEY + reg_date
    req = requests.get(target_url)
    is_ok = req.ok
    return is_ok

def extract_urls():
    None

