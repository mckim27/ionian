#! /usr/bin/python
# -*- coding: utf-8 -*-
class ExitException(Exception):
    __exit_code = 1

    def __init__(self, message, exit_code):
        super().__init__(message)

        self.__exit_code = exit_code

    def exit(self):
        exit(self.__exit_code)

class CannotRunException(ExitException):
    def __init__(self, message, exit_code):
        super().__init__(message, exit_code)

class CollectorException(ExitException):
    def __init__(self, message, exit_code):
        super().__init__(message, exit_code)