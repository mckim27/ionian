#! /usr/bin/python
# -*- coding: utf-8 -*-

import traceback
import python_pachyderm
import time
import sys
from init import constant
from logzero import logger as log


class PachdRepoStorer:

    __client = None
    __commit = None
    __repo_name = None
    __branch = None
    __file_list = []
    __pre_commit_id = None

    def __init__(self, repo_name, branch: str = 'master'):
        self.__client = python_pachyderm.PfsClient(
            host=constant.CONFIG['pachd_host'], port=constant.CONFIG['pachd_port'])

        self.__repo_name = repo_name
        self.__branch = branch

    def put_file_str(self, file_path, contents: str):
        pachd_data = {
            'file_path': file_path,
            'contents': contents
        }

        self.__file_list.append(pachd_data)

    def reset(self):
        self.__commit = None
        self.__file_list.clear()

    def put_file_atomic(self, file_path, contents: str):

        pachd_data = {
            'file_path': file_path,
            'contents': contents
        }

        try:
            self.__commit = self.__client.start_commit(
                self.__repo_name, self.__branch, parent=self.__pre_commit_id)

            self.__client.put_file_bytes(
                self.__commit, pachd_data['file_path'], pachd_data['contents'].encode('utf-8')
            )

            self.__client.finish_commit(self.__commit)
            log.info('finish pachd commit. commit_id : {}'.format(self.__commit.id))

            self.__pre_commit_id = self.__commit.id

            self.__commit = None

        except Exception as e:
            if 'has not been finished' in traceback.format_exc():
                log.warn('the parent commit has not been finished. wait a moment ...')
                time.sleep(5)

                self.put_file_atomic(file_path, contents)
            else:
                raise e

    def commit(self):
        try:
            self.__commit = self.__client.start_commit(
                self.__repo_name, self.__branch, parent=self.__pre_commit_id)

            log.info('start pfs commit !! commit id : {}'.format(self.__commit.id))

            for idx, pachd_data in enumerate(self.__file_list):
                self.__client.put_file_bytes(
                    self.__commit, pachd_data['file_path'], pachd_data['contents'].encode('utf-8')
                )
                log.info('seq : {}, put file success. file : {}'.format(idx + 1, pachd_data['file_path']))

            self.__client.finish_commit(self.__commit)

            log.info('finish pfs commit. commit_id : {}'.format(self.__commit.id))

            self.__pre_commit_id = self.__commit.id

        except Exception as e:
            if 'has not been finished' in traceback.format_exc():
                log.warn('the parent commit has not been finished. wait a moment ...')
                time.sleep(5)

                self.commit()
            else:
                raise e
