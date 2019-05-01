# -*- coding: utf-8 -*-

class Collector :

    def collect(self, work_func):
        self.__result = work_func()

    def save_result(self):
        None