#! /usr/bin/python
# -*- coding: utf-8 -*-

import python_pachyderm
from init import constant
from logzero import logger as log


class PachdRepoStorer:

    __client = None
    __commit_id = None
    __repo_name = None
    __branch = None

    def __init__(self, repo_name, branch: str = 'master'):
        self.__client = python_pachyderm.PfsClient(
            host=constant.CONFIG['pachd_host'], port=constant.CONFIG['pachd_port'])

        self.__repo_name = repo_name
        self.__branch = branch

    def put_file_str(self, file_path, data: str):
        if self.__commit_id is None:
            self.__commit_id = self.__client.start_commit(self.__repo_name, self.__branch)

        log.info('pachd put-file path : {}'.format(file_path))

        self.__client.put_file_bytes(self.__commit_id, file_path, data.encode('utf-8'))

    def commit(self):
        self.__client.finish_commit(self.__commit_id)
        self.__commit_id = None
