#! /usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Parser(ABC) :

    @abstractmethod
    def waiting_and_parsing(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def stop(self):
        pass