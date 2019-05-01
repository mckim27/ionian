# -*- coding: utf-8 -*-
from collect.collector import Collector
from collect.daumnews_collector import collect as dnews_col_func

if __name__ == "__main__" :
    collector = Collector()
    work_func = dnews_col_func

    collector.collect(work_func)
