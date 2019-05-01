# -*- coding: utf-8 -*-
import requests
import bs4
import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://media.daum.net'

def collect():
    publish_date = datetime.datetime.now()
    publish_date -= datetime.timedelta(days=1)
    publish_date = publish_date.strftime("%Y%m%d")

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

    return sub_cate_urlpaths

def extract_urls (target_url):
    None