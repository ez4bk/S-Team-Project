# coding=utf-8
from abc import abstractmethod


class ProcessInterface(object):

    @abstractmethod
    def run(self):
        pass
