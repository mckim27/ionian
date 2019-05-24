#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log


def assert_str_default(text):
    assert text is not None and type(text) is str, \
        'input text is invalidate ... text : {0}'.format(text)


def assert_str_and_empty(text):
    assert text is not None and type(text) is str and text.strip() != '', \
        'input text is invalidate ... text : {0}'.format(text)


def assert_str_and_length(text, text_len):
    assert text is not None and type(text) is str and len(text) == text_len, \
        'input text is invalidate ... text : {0}'.format(text)

# 추후 데이터 보면서 판단.
def is_short_text(text):
    min_text_len = 1

    if len(text) < min_text_len:
        return True
    else:
        return False


def is_empty_text(text):
    if text.strip() == '':
        log.warn('input text is empty ...')

        return True
    else:
        return False




