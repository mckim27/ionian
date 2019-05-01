# -*- coding: utf-8 -*-
import requests
import bs4
import datetime
from bs4 import BeautifulSoup

def collect():
    base_url = 'https://media.daum.net/breakingnews'

    publish_date = datetime.datetime.now()
    publish_date -= datetime.timedelta(days=1)
    publish_date = publish_date.strftime("%Y%m%d")

    # 2019-05-02 기준 daum news category.
    # 각 category 에 따라 api path 마지막이 결정됨. 컬럼과 보도자료는 사용 안함.
    category_root_tailpaths = [
        'society',
        'politics',
        'economic',
        'foreign',
        'culture',
        'entertain',
        'sports',
        'digital'
    ]

    for tailpath in category_root_tailpaths:
        target_url = base_url + '/' + tailpath

        req = requests.get(target_url)
        html = req.text

        header = req.headers
        status = req.status_code
        is_ok = req.ok

        soup = BeautifulSoup(html, 'html.parser')

        # tab_nav2_el = soup.find('ul', class_='tab_nav2')
        # # print(type(tab_nav2))
        # for el in tab_nav2_el:
        #     if type(el) is not bs4.element.NavigableString:
        #         print(el.find('a', class_='link_tab').get('href'))
        # # link_tab_el = soup.find('a', class_='link_tab')
        # # print(link_tab_el)
