#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2019/12/10 16:43
"""
import os
import traceback

from jsonpath import jsonpath
from commonlib.api_protocol_lib.api_exchange import api_exchange_http
from commonlib.api_protocol_lib.base_info.base_utils import BaseUtils

from commonlib.api_protocol_lib.http_head_set import http_get_cookie
from commonlib.base_lib.mylog.mylog import log

RCCP_PROTOCOL = 'https'
RCCP_LOGIN_API_NAME = '/rccp/base/admin/loginAdmin'
RCCP_CONTENT_TYPE = 'application/json'

rccp_cookies = {}

cert_base_path = os.path.abspath(os.path.join(__file__, "..", "cert"))
cert_client_crt = os.path.join(cert_base_path, "rccpclient.crt")
cert_client_key = os.path.join(cert_base_path, "rccpclient.key")


class RccpBaseInfo(BaseUtils):

    def __init__(self, server_ip, port, user_name, user_pwd):
        self.__headers = None
        self.__cookie = ""
        self.server_ip = server_ip
        self.port = port
        self.user_name = user_name
        self.user_pwd = user_pwd

        self.content_type = RCCP_CONTENT_TYPE
        try:
            self.get_cookies(user_name, user_pwd)
        except Exception as e:
            log(traceback.format_exc())
            raise e
        self.__get_default_header()

    @staticmethod
    def cert_api_exchange(url, param, method, **kwargs):
        result = api_exchange_http(url, param, method, cert=(cert_client_crt, cert_client_key), **kwargs)
        return result

    def get_cookies(self, name, pwd, flag=False):
        global rccp_cookies
        if self.server_ip in rccp_cookies and rccp_cookies[self.server_ip] != "" and not flag:
            url = f'{RCCP_PROTOCOL}://{self.server_ip}:{self.port}/rccp/base/admin/getCurrentUserInfo'
            headers = {'Content-Type': self.content_type, 'cookie': rccp_cookies[self.server_ip]}
            result = api_exchange_http(url=url, param={}, method='post', headers=headers)
            if not jsonpath(result.json(), '$..status')[0] == 'SUCCESS':
                rccp_cookies[self.server_ip] = ""
        if self.server_ip not in rccp_cookies or rccp_cookies[self.server_ip] == "" or flag:
            http_url = f'{RCCP_PROTOCOL}://{self.server_ip}:{self.port}{RCCP_LOGIN_API_NAME}'
            rccp_cookies[self.server_ip] = http_get_cookie(login_url=http_url, user_name=name, user_pwd=pwd)
        self.__cookie = rccp_cookies[self.server_ip]
        return rccp_cookies[self.server_ip]

    @staticmethod
    def base_assert(result):
        if jsonpath(result.json(), '$..status'):
            assert result.json()['status'] != 'NO_LOGIN'

    def get_current_cookies(self):
        global rccp_cookies
        self.__cookie = rccp_cookies[self.server_ip]
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
        global rccp_cookies
        self.__cookie = rccp_cookies[self.server_ip]
        if "cookie" in self.__headers:
            self.__headers["cookie"] = self.__cookie
        return self.__headers

    def set_header(self, headers):
        self.__headers = headers


if __name__ == "__main__":
    pass
