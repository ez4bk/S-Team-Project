# coding=utf-8

# coding=utf-8
import json
import traceback

import requests
from simplejson import JSONDecodeError

from commonlib.api_protocol_lib.http_head_set import base_head_info
from commonlib.base_lib.mylog.mylog import log

requests.packages.urllib3.disable_warnings()
retry_time = 3  # 返回10060（网络原因导致请教失败）时，重试次数
HTTPS_CONTENT_TYPE = 'application/json'


def api_verify(**kwargs):
    requests.packages.urllib3.disable_warnings()
    allow_redirects = False
    verify = False
    cert = None
    if 'allow_redirects' in kwargs:
        allow_redirects = kwargs['allow_redirects']
        del kwargs["allow_redirects"]
    if "verify" in kwargs:
        verify = kwargs["verify"]
        del kwargs["verify"]
    if "cert" in kwargs:
        cert = kwargs["cert"]
        del kwargs["cert"]
    return allow_redirects, verify, cert, kwargs


def get(url, params=None, **kwargs):
    """
    http get请求
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    for a in range(retry_time):
        try:
            allow_redirects, verify, cert, kwargs = api_verify(**kwargs)
            return __get_do(url, params, allow_redirects=allow_redirects, verify=verify, cert=cert, **kwargs)
        except ConnectionError as e:
            if a < retry_time - 1:
                log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < retry_time - 1:
                    log("retry get request time:" + str(a + 1))
                    continue
                else:
                    raise e
            else:
                raise e


def __get_do(url, params=None, **kwargs):
    """
    http get请求
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    log("--->http request get :" + str(url))
    if params != "":
        log("data:" + str(params))
    result = requests.get(url, params=params, **kwargs)
    log("<---response " + str(result.status_code))
    # try:
        # log(str(result.json()))
    # except JSONDecodeError:
    #     pass
    return result


def post(url, data=None, **kwargs):
    """
    http post 请求
    :param url:
    :param data:
    :param kwargs:
    :return:
    """

    for a in range(3):
        try:
            allow_redirects, verify, cert, kwargs = api_verify(**kwargs)
            return __post_do(url, data, allow_redirects=allow_redirects, verify=verify, cert=cert, **kwargs)
        except ConnectionError as e:
            if a < retry_time - 1:
                log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < retry_time - 1:
                    log("retry post request time:" + str(a + 1) + ":" + msg)
                    continue
                else:
                    raise e
            else:
                raise e


def __post_do(url, data=None, **kwargs):
    """
    http post 请求
    :param url:
    :param data:
    :param kwargs:
    :return:
    """
    log("--->http request post :" + str(url))
    if data != "" and not str(data).__contains__('application/octet-stream'):
        log("data:" + str(data))
    if type(data) == dict:
        if url.endswith('.php') or url.__contains__('chunk'):
            # log("data type dict does not need to change")
            pass
        else:
            data = json.dumps(data)
    if 'files' in kwargs:
        log('files:{}'.format(kwargs['files']))
    result = requests.post(url, data=data, **kwargs)
    result.raise_for_status()
    log("<---response " + str(result.status_code))
    try:
        log(str(result.json()))
    except JSONDecodeError:
        pass
    return result


def put(url, data=None, **kwargs):
    """
    http put 请求
    :param url:
    :param data:
    :param kwargs:
    :return:
    """
    for a in range(3):
        try:
            allow_redirects, verify, cert, kwargs = api_verify(**kwargs)
            return __put_do(url, data, allow_redirects=allow_redirects, verify=verify, cert=cert, **kwargs)
        except ConnectionError as e:
            if a < retry_time - 1:
                log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < retry_time - 1:
                    log("retry put request time:" + str(a + 1))
                    continue
                else:
                    raise e
            else:
                raise e


def __put_do(url, data=None, **kwargs):
    """
    http put 请求
    :param url:
    :param data:
    :param kwargs:
    :return:
    """
    log("--->http request put :" + str(url))
    if data != "":
        log("data:" + str(data))
    if type(data) == dict:
        data = json.dumps(data)
    result = requests.put(url, data=data, **kwargs)
    result.raise_for_status()
    log("<---response " + str(result.status_code))
    try:
        log(str(result.json()))
    except JSONDecodeError:
        pass
    return result


def delete(url, param, **kwargs):
    """
    http delete 请求
    :param param:
    :param url:
    :param kwargs:
    :return:
    """
    for a in range(3):
        try:
            return __delete_do(url, param, **kwargs)
        except ConnectionError as e:
            if a < retry_time - 1:
                log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < retry_time - 1:
                    log("retry put request time:" + str(a + 1))
                    continue
                else:
                    raise e
            else:
                raise e


def __delete_do(url, param, **kwargs):
    """
    http delete 请求
    :param url:
    :param kwargs:
    :return:
    """
    log("--->http request delete :" + str(url))
    allow_redirects, verify, cert, kwargs = api_verify(**kwargs)
    if "json" in kwargs:
        result = requests.delete(url, data=param, allow_redirects=allow_redirects, verify=verify, cert=cert, **kwargs)
    else:
        result = requests.delete(url, data=param, allow_redirects=allow_redirects, verify=verify, cert=cert, **kwargs)
    result.raise_for_status()
    log("<---response " + str(result.status_code))
    try:
        log(str(result.json()))
    except JSONDecodeError:
        pass
    return result


class HttpInterface(object):

    @staticmethod
    def exchange(url, param, request_type, **kwargs):
        if 'headers' not in kwargs:
            if url.__contains__('.php'):
                log('php do not need content_type ')
            else:
                content_type = HTTPS_CONTENT_TYPE
                headers = base_head_info(content_type=content_type)
                kwargs['headers'] = headers
        result = None
        if str(request_type).lower() == "get":
            result = get(url, param, **kwargs)
        elif str(request_type).lower() == "put":
            result = put(url, param, **kwargs)
        elif str(request_type).lower() == "post":
            result = post(url, param, **kwargs)
        elif str(request_type).lower() == "delete":
            result = delete(url, param, **kwargs)
        else:
            log("request does not support")
        return result
