# coding=utf-8
from abc import abstractmethod


class RunnerSetup(object):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def tear_down(self):
        pass
