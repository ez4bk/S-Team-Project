#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2019/12/10 16:43
"""
import traceback

from jsonpath import jsonpath
from commonlib.api_protocol_lib.api_exchange import api_exchange_http
from commonlib.api_protocol_lib.base_info.base_utils import BaseUtils

from commonlib.api_protocol_lib.http_head_set import http_get_cookie
from commonlib.base_lib.mylog.mylog import log

RCDC_PROTOCOL = 'https'
RCDC_LOGIN_API_NAME = '/rcdc/rco/admin/loginAdmin'
RCDC_CONTENT_TYPE = 'application/json'

rcdc_cookies = {}


class RcdcBaseInfo(BaseUtils):

    def __init__(self, server_ip, port, user_name, user_pwd):
        self.__headers = None
        self.__cookie = rcdc_cookies
        self.server_ip = server_ip
        self.port = port
        self.user_name = user_name
        self.user_pwd = user_pwd

        self.content_type = RCDC_CONTENT_TYPE
        try:
            self.get_cookies(user_name, user_pwd)
        except Exception as e:
            log(traceback.format_exc())
            raise e
        self.__get_default_header()

    # @staticmethod
    # def cert_api_exchange(url, data, method, **kwargs):
    #     result = api_exchange_http(url, data, method, cert=(RCCP_CERT_CRT_DIR, RCCP_CERT_KEY_DIR), **kwargs)
    #     return result

    def get_cookies(self, name, pwd, flag=False):
        global rcdc_cookies
        if self.server_ip in rcdc_cookies and rcdc_cookies[self.server_ip] != "" and not flag:
            url = f'{RCDC_PROTOCOL}://{self.server_ip}:{self.port}/rcdc/rco/admin/getCurrentUserInfo'
            headers = {'Content-Type': self.content_type, 'cookie': rcdc_cookies[self.server_ip]}
            result = api_exchange_http(url=url, param={}, method='post', headers=headers)
            if not jsonpath(result.json(), '$..status')[0] == 'SUCCESS':
                rcdc_cookies[self.server_ip] = ""
        if self.server_ip not in rcdc_cookies or rcdc_cookies[self.server_ip] == "" or flag:
            http_url = f'{RCDC_PROTOCOL}://{self.server_ip}:{self.port}{RCDC_LOGIN_API_NAME}'
            rcdc_cookies[self.server_ip] = http_get_cookie(login_url=http_url, user_name=name, user_pwd=pwd)
        self.__cookie = rcdc_cookies[self.server_ip]
        return rcdc_cookies[self.server_ip]

    def get_current_cookies(self):
        global rcdc_cookies
        self.__cookie = rcdc_cookies[self.server_ip]
        return self.__cookie

    def __get_default_header(self):
        if self.__cookie:
            headers = {'Content-Type': self.content_type, 'cookie': self.__cookie}
            log('<---request header %s' % headers)
        else:
            headers = {'Content-Type': self.content_type}
            log('<---request header %s' % headers)
        self.__headers = headers
        return headers

    def get_current_header(self):
        global rcdc_cookies
        self.__cookie = rcdc_cookies[self.server_ip]
        if "cookie" in self.__headers:
            self.__headers["cookie"] = self.__cookie
        log("current header is " + str(self.__headers))
        return self.__headers

    def set_header(self, headers):
        self.__headers = headers


if __name__ == "__main__":
    RcdcBaseInfo("172.28.100.159", 8443, "admin", "Admin123")
