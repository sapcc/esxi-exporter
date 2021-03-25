from functools import  lru_cache

import json
import logging

import yaml

logger = logging.getLogger('esxi')


class FileHelper:
    """
    Providing functionality to read text-files, yaml-files and json-files.
    """


    @staticmethod
    def read_utf8_file(path) -> str:
        """
        Reads a file with utf-8 encoding and returns a string

        :param path: the file path
        :return: return file content as string or None
        """
        with open(path, 'rt', encoding='utf8') as f:
            data = f.read()
        return data

    @staticmethod
    @lru_cache(maxsize=1)
    def get_yaml_dict(path: str) -> dict:
        """
        Load yaml file as dictionary

        :param path: The path to the yaml file.
        :return: the yaml-file parsed to a dict
        """
        with open(path, 'rt', encoding='utf8') as f:
            data = yaml.safe_load(f)
        return data


    @staticmethod
    def get_json_dict(path: str) -> dict:
        """
        Load json file as dictionary.

        :param path: The path to the json file.
        :return: the json-file parsed to a dict
        """

        with open(path, 'rt', encoding='utf8') as f:
            data = json.load(f)
        return data
