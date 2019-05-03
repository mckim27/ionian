#! /usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Collector(ABC) :

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def store(self):
        pass