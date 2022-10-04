# coding = utf-8
from abc import abstractmethod


class ApiInterface(object):

    def __init__(self):
        pass

    @abstractmethod
    def exchange(self, url, param, **kwargs):

        pass
