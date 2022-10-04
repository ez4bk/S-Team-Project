# coding=utf-8

from jsonpath import jsonpath

from lib.commonlib.base_lib.mylog.mylog import log


class BaseUtils(object):
    @staticmethod
    def common_assert(result, msgArgArr=None, msgKey=None, message=None, content=None, status=None, code=-999):
        log('<<<<<<<<<<<<<common_assert公用验证')
        if msgArgArr:
            assert jsonpath(result, '$..msgArgArr')[0].__contains__(msgArgArr)
        if msgKey:
            assert jsonpath(result, '$..msgKey')[0].__contains__(msgKey)
        if message:
            assert jsonpath(result, '$..message')[0].__contains__(message)
        if content:
            assert jsonpath(result, '$..content')[0].__contains__(content)
        if code != -999:
            assert jsonpath(result, '$..code') == code
        if content:
            assert jsonpath(result, '$..status')[0] == status
