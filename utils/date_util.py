#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime


def get_previous_day(pre, format) :
    result = datetime.datetime.now()
    result -= datetime.timedelta(days=pre)
    return result.strftime(format) #("%Y%m%d")

