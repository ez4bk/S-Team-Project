# coding=utf-8
import traceback
from abc import abstractmethod

from lib.commonlib.base_lib.mylog.mylog import log, log_e
from lib.commonlib.common_frame import frame_utils
from lib.commonlib.common_frame.frame_runner import FrameRunner, NEXT_TYPE_CONTINUE, NEXT_TYPE_BLOCK

deploy_type = ""


class DeployFrame(FrameRunner):

    def __init__(self, host_ip, runner_id, runner_setup=None, out_obj=None, show_callback=None):
        super().__init__(runner_id)
        self.__runner_setup = runner_setup
        self._cookies = ""
        self._ssh_client = ""
        self._host_ip = host_ip
        self._out_obj = out_obj
        self._show_callback = self._get_call_back(out_obj, show_callback)

    @staticmethod
    def __do_run(func):  # 支持不同返回处理
        try:
            log("begin to run " + str(func))
            result = func()
            if result is None:
                return NEXT_TYPE_CONTINUE, ""
            elif len(result) == 2:
                return result
            return result[0], result[1]
        except Exception:
            log_e(traceback.format_exc())
            return NEXT_TYPE_BLOCK, str(traceback.format_exc())

    def run(self, show_log_func=None):
        print("deploy type is >>>" + str(deploy_type))
        print("4444444444>>>" + self._cookies)
        if deploy_type == "env_deploy":
            return self.__do_run(self.step)
        else:
            return self.__do_run(self.check)

    def tear_down(self):
        pass

    def setup(self):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def check(self):
        pass

    def env_deploy(self, retry=False):
        global deploy_type
        deploy_type = "env_deploy"
        frame_utils.set_retry_flag(retry)
        if retry:
            frame_utils.clear_runner_result()
        return self.runner(self)

    def env_check(self, retry=False):
        global deploy_type
        deploy_type = "deploy_check"
        frame_utils.set_retry_flag(retry)
        if retry:
            frame_utils.clear_runner_result()
        return self.runner(self)

    def runner(self, runner_list, setup=False, error_continue=False, **kwargs):
        return super().runner(runner_list, self._show_callback, setup, error_continue)

    def _get_call_back(self, out_obj, show_log):
        if show_log is not None:
            return show_log
        while True:
            if hasattr(out_obj, "_show_callback"):
                if getattr(out_obj, "_show_callback") is not None:
                    return getattr(out_obj, "_show_callback")
                else:
                    if hasattr(out_obj, "_out_obj") and getattr(out_obj, "_out_obj") is not None:
                        return self._get_call_back(getattr(out_obj, "_out_obj"), None)
                    else:
                        return None
            return None
