#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import tempfile
import threading
import time
import traceback

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log_e


class MyOs:
    obj = subprocess.Popen

    def __init__(self):
        pass

    def process(self, cmd, stdout=None):
        """
            执行CMD指令，返回相应的执行结果。阻塞函数，无法执行如logcat或top等指令

            :param stdout:
            :type cmd:str 指令名称
            :rtype: list
        """
        result = self.execute(cmd, stdout)
        return self.parseResult(result)

    def cmdParse(self, cmd):
        """
            解析指令列表，如['adb','devices','-l']，解析成'adb devices -l'
            :type cmd:list 指令列表
            :rtype: str
        """
        data = ''
        if isinstance(cmd, str):  # 如果传入的为string类型，直接作为指令
            data = cmd
            return data
        for info in cmd:
            tmp = info + " "
            data += tmp
        return data

    def execute(self, cmd, stdout=None):
        """
        stdout=subprocess.PIPE
        :param cmd:
        :param stdout:
        :return:
        """
        try:
            out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1024)
            if stdout is None:
                fileNo = out_temp.fileno()
            else:
                fileNo = stdout
            self.obj = subprocess.Popen(cmd, stdout=fileNo, stderr=fileNo, shell=True)
            self.obj.wait()
            out_temp.seek(0)
            if stdout is None:
                result = out_temp.readlines()
            else:
                result = self.obj.stdout.readlines()
            return result
        except Exception as e:
            _commonlib_log_e(e)
            _commonlib_log_e(traceback.format_exc())

    def process_a(self, cmd):
        """
            执行CMD指令，返回相应的执行结果。阻塞函数，无法执行如logcat或top等指令
            :type cmd:str 指令名称
            :rtype: list
        """
        result = self.execute_a(cmd)
        return self.parseResult(result)

    def execute_a(self, cmd):
        try:
            out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1024)
            fileNo = out_temp.fileno()
            self.obj = subprocess.Popen(cmd, stdout=fileNo, stderr=fileNo, shell=True)
            run_thread = threading.Thread(target=self.thread_out, args=(self.obj, out_temp), name='test_task_begin')
            run_thread.start()
            self.obj.wait()
            out_temp.seek(0)
            return out_temp.readlines()
        except Exception as e:
            _commonlib_log_e(e)
            _commonlib_log_e(traceback.format_exc())

    def exec(self, cmd, stdout=None):
        """
            执行CMD指令，返回相应的执行结果。阻塞函数，无法执行如logcat或top等指令

            :param stdout:
            :type cmd:str 指令名称
            :rtype: list
        """
        result = self.execute(cmd, stdout)
        return result

    def thread_out(self, pro_obj, out_input):
        pass

    def show_message(self, pro_obj, msg):
        pass

    def destroy(self):
        self.obj.terminate()

    def parseResult(self, result):
        resultList = []
        if result is None:
            return resultList
        for data in result:
            while True:
                if data == '':
                    break
                if data[-1] == '\r' or data[-1] == '\n':
                    data = data[0:-1]
                else:
                    resultList.append(data)
                    break
        return resultList

    @staticmethod
    def getCurrentTime(format="%Y-%m-%d %H:%M:%S"):
        return time.strftime(format, time.localtime(time.time()))


debug = MyOs()
if __name__ == '__main__':
    pass
    # print(debug.execute("dir C: | find \"可用字节\""))
    # path = "E:\UmsAutoTest"+"\\"+"recordera"
    # cmd = "pytest -k test_login -v --junitxml=test_one_func1.xml"
    # pytest.main(["-k","test_login","-v"])
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
    # for line in iter(p.stdout.readline, b''):
    #     loge(line)
    # p.stdout.close()
    # p.wait()
    # p.terminate()
    # my_os = MyOs()
    # my_os.process_a("ping 127.0.0.1 -t")
