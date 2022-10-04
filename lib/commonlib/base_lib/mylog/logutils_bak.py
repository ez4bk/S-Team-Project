#!/usr/bin/env python
#   coding=utf-8
"""
 @Time    : 2019/1/23 10:41
 @Author  : niewn
 @Site    : 
 @File    : LogUtils.py
 @Software: PyCharm
 @license : Copyright(C), RuiJie 
 @Contact : niewenna@ruijie.com.cn 
 @Date  : 2019/1/23
 @Desc  : 日志文件，线程级别
"""
import datetime
import logging
import os
import time
from logging import handlers

from lib.commonlib.base_lib.utils.processpath import cur_file_dir


class LogUtils:

    def __init__(self, tag, log_cate="sys_api_test_result", level='info', when='H', backCount=6,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', ):
        """日志文件夹不存在则创建"""
        # self.log_time = time.strftime("%Y_%m_%d_%h_%M")
        self.log_time = time.strftime('%Y_%m_%d_%H', time.localtime(time.time()))
        print(">>>>>" + str(cur_file_dir()))
        file_dir = cur_file_dir() + "\\mylog"
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        self.log_path = file_dir
        self.log_name = self.log_path + log_cate + "." + self.log_time + '.mylog'

        self.logger = logging.getLogger(tag)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        self.sh = logging.StreamHandler()  # 往屏幕上输出
        self.sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=self.log_name, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(self.sh)  # 把对象加到logger里
        self.logger.addHandler(th)
        self.sh.close()
        th.close()

    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def get_logger(self):
        return self.logger

    @staticmethod
    def set_log_path(log_path):
        global logger
        global fh
        global ch
        global formatter
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logger.removeHandler(fh)
        logger.removeHandler(ch)
        logger = logging.getLogger("TC")
        logger.setLevel(logging.INFO)
        log_file = log_path + "\\" + str(
            datetime.datetime.now().strftime("%Y-%m-%d")) + ".mylog"
        fh = logging.FileHandler(log_file, encoding="UTF-8")
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)


#
# import logging.handlers
#
# log_file = 'test.mylog'
#
# time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='S', interval=3, backupCount=0)
# time_handler.suffix = 'test-%Y-%m-%d-%S.mylog'
# time_handler.setLevel('INFO')  # error以上的内容输出到文件里面
#
# fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
# formatter = logging.Formatter(fmt)
# time_handler.setFormatter(formatter)
#
# logger = logging.getLogger('updateSecurity')
# logger.setLevel('INFO')
# logger.addHandler(time_handler)
#
# ch = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
# ch.setFormatter(formatter)
# logger.addHandler(ch)
#
#
# index = 0
# while True:
#     index += 1
#     logger.info(">>>>>>>>>" + str(index))
#     time.sleep(1)
#     break
#

if __name__ == '__main__':
    LogUtils("demo").get_logger().info("abc")
