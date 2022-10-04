# coding=utf-8
import time
from abc import abstractmethod

from lib.commonlib.base_lib.mylog.mylog import log
from lib.commonlib.common_frame import frame_utils
from lib.commonlib.common_frame.frame_utils import load_runner_result, save_runner_result
from lib.commonlib.common_frame.runner import Runner
from lib.commonlib.common_frame.runner_setup import RunnerSetup

NEXT_TYPE_BLOCK = "next_type_block"
NEXT_TYPE_ERROR = "next_type_error"
NEXT_TYPE_WARMING = "next_type_warming"
NEXT_TYPE_CONTINUE = "next_type_continue"
NEXT_TYPE_SUCCESS = "next_type_success"
NEXT_TYPE_RUNNING = "next_type_running"


class FrameRunner(Runner, RunnerSetup):

    @abstractmethod
    def run(self, show_log_func=None):
        pass

    @abstractmethod
    def tear_down(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @staticmethod
    def __show_log_utils(show_log_fun, msg):
        if show_log_fun is None:
            log(">>>" + msg)
        else:
            show_log_fun(msg)

    def runner(self, runner_list, show_log_func=None, setup=False, error_continue=False):
        flag, result, runner_id = NEXT_TYPE_CONTINUE, "", ""
        if type(runner_list) is not list:
            runner_list = [runner_list]
        retry = self.__get_retry_flag()
        runner_id_list = self.__get_runner_id_list(runner_list)
        begin_time = time.time()
        if len(runner_list) > 1:  # 减少冗余的界面提示信息
            self.__show_log_utils(show_log_fun=show_log_func, msg=f"执行 {str(runner_id_list)} 步骤...")
        for runner in runner_list:
            flag, result = self.__runner_do(runner, retry=retry, show_log_func=show_log_func, setup=setup)
            if flag == NEXT_TYPE_BLOCK:
                break
            if flag == NEXT_TYPE_ERROR and not error_continue:
                break
        cost_time = time.time() - begin_time
        if flag == NEXT_TYPE_ERROR:  # 如果所有列表中有包含失败时，此步骤返回不可继续往下
            flag = NEXT_TYPE_BLOCK
        if len(runner_list) > 1:  # 减少冗余的界面提示信息
            self.__show_log_utils(show_log_fun=show_log_func,
                                  msg=f"执行 {str(runner_id_list)} 返回 {get_msg_by_flag(flag)} ,耗时 {str(cost_time)}")
        return flag, result

    def __runner_do(self, runner, retry=False, show_log_func=None, setup=False):
        """
        :type   runner  Runner
        :param runner:
        :param retry:
        :param show_log_func:
        :return:
        """
        runner_id = runner._runner_id
        flag, msg = NEXT_TYPE_CONTINUE, ""
        begin_time = time.time()
        self.__show_log_utils(show_log_fun=show_log_func, msg=f"\r\n执行 {runner_id} 步骤...")
        if retry or not self.__has_do_before(runner_id, show_log_func):
            self.__save_runner_result(runner_id, NEXT_TYPE_RUNNING)
            if setup:
                self.setup()
                self.__init_param(runner, self)
            else:
                if runner._out_obj is not None:
                    self.__init_param(runner, runner._out_obj)
            flag, msg = runner.run()
            if setup:
                self.tear_down()
            self.__save_runner_result(runner_id, flag)
        cost_time = time.time() - begin_time
        self.__show_log_utils(show_log_fun=show_log_func,
                              msg=f"执行 {runner_id} " + get_msg_by_flag(flag) + "，耗时 " + str(cost_time))
        return flag, msg

    def __has_do_before(self, runner_id, show_log_func):
        config = load_runner_result()
        if runner_id in config and config[runner_id]["flag"] == NEXT_TYPE_CONTINUE:
            self.__show_log_utils(show_log_fun=show_log_func, msg=f"\r\nrunner id " + str(runner_id) + " has do before")
            return True
        return False

    @staticmethod
    def __save_runner_result(runner_id, flag):
        config = load_runner_result()
        if runner_id in config:
            tmp = config[runner_id]
        else:
            tmp = {}
        tmp["flag"] = flag
        config[runner_id] = tmp
        save_runner_result(config)

    @staticmethod
    def __get_runner_id_list(runner_list):
        """
        :type   runner_list list
        :param runner_list:
        :return:
        """
        tmp_list = []
        for runner in runner_list:
            tmp_list.append(runner._runner_id)
        return tmp_list

    @staticmethod
    def __get_retry_flag():
        return frame_utils.get_retry_flag()

    def __init_param(self, runner, obj):
        runner._cookies = obj._cookies
        runner._ssh_client = obj._ssh_client


def get_msg_by_flag(flag):
    if flag == NEXT_TYPE_BLOCK:
        return "失败阻塞"
    if flag == NEXT_TYPE_ERROR:
        return "失败"
    if flag == NEXT_TYPE_CONTINUE:
        return "成功"
    return "未知"
