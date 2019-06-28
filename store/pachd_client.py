#! /usr/bin/python
# -*- coding: utf-8 -*-

import traceback
import python_pachyderm
from init import constant
from logzero import logger as log


class PachdRepoStorer:

    __client = None
    __commit_id = None
    __repo_name = None
    __branch = None
    __is_complete = False
    __file_list = []

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

    def commit(self, retry_count: int = 0):
        try:
            self.__commit_id = self.__client.start_commit(self.__repo_name, self.__branch)

            for pachd_data in self.__file_list:
                self.__client.put_file_bytes(
                    self.__commit_id, pachd_data['file_path'], pachd_data['contents'].encode('utf-8')
                )

            self.__client.finish_commit(self.__commit_id)

            log.info('finish pachd commit. commit_id : {}'.format(self.__commit_id))
            self.__is_complete = True

        except Exception as e:
            log.error(traceback.format_exc())

            self.__client.delete_commit(self.__commit_id)

            if retry_count < 3:
                self.commit(retry_count + 1)
            else:
                is_complete = True
                raise e
            
        finally:
            if self.__is_complete:
                self.__commit_id = None
                self.__file_list.clear()
                self.__is_complete = False