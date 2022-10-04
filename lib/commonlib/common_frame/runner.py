# coding=utf-8
from abc import abstractmethod


class Runner(object):

    def __init__(self, runner_id):
        self._runner_id = runner_id

    @abstractmethod
    def run(self, show_log_func=None):
        pass

