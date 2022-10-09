# coding=utf-8
import json
import time
import traceback

import requests
from simplejson import JSONDecodeError

from lib.base_lib.mylog.mylog import _commonlib_log

__retry_time = 3

"""
aaa
"""


def get(url, params=None, **kwargs):
    """
    http或https get请求

    :param url: 请求的url
    :param params:  请求的参数，默认为None
    :param kwargs:  可变参数，可参照request类。通常可变参中需要 headers 如：headers = {'Content-Type': 'application/json'}

    :return: 返回 请求响应，如果是json类型，可以通过response.json()获取返回的json串
    """
    for a in range(__retry_time):
        try:
            return __get_do(url, params, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < __retry_time - 1:
                    _commonlib_log("retry get request time:" + str(a + 1))
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
    _commonlib_log("--->http request get :" + str(url))
    if params != "":
        _commonlib_log("data:" + str(params))
    result = requests.get(url, params=params, verify=False, **kwargs)
    _commonlib_log("<---response " + str(result.status_code))
    try:
        _commonlib_log(str(result.json()))
    except JSONDecodeError:
        pass
    return result


def post(url, data=None, json_data=None, **kwargs):
    """
    http或https post请求

    :param url: 请求的url
    :param data:  请求的参数，默认为None
    :param json_data:  请求的参数，默认为None
    :param kwargs:  可变参数，可参照request类。通常可变参中需要 headers 如：headers = {'Content-Type': 'application/json'}

    :return: 返回 请求响应，如果是json类型，可以通过response.json()获取返回的json串
    """
    for a in range(3):
        try:
            return __post_do(url, data, json_data, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < __retry_time - 1:
                    _commonlib_log("retry post request time:" + str(a + 1))
                    continue
                else:
                    raise e
            else:
                raise e


def __post_do(url, data=None, json_data=None, **kwargs):
    """
    http post 请求
    :param url:
    :param data:
    :param json_data:
    :param kwargs:
    :return:
    """
    _commonlib_log("--->http request post :" + str(url))
    if data != "":
        _commonlib_log("data:" + str(data))
    if type(data) == dict:
        data = json.dumps(data)
    result = requests.post(url, data=data, json=json_data, allow_redirects=False, verify=False, **kwargs)
    result.raise_for_status()
    _commonlib_log("<---response " + str(result.status_code))
    try:
        _commonlib_log(str(result.json()))
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
            return __put_do(url, data, allow_redirects=False, **kwargs)
        except ConnectionError as e:
            if a < __retry_time - 1:
                _commonlib_log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < __retry_time - 1:
                    _commonlib_log("retry put request time:" + str(a + 1))
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
    _commonlib_log("--->http request put :" + str(url))
    if data != "":
        _commonlib_log("data:" + str(data))
    if type(data) == dict:
        data = json.dumps(data)
    result = requests.put(url, data=data, verify=False, **kwargs)
    result.raise_for_status()
    _commonlib_log("<---response " + str(result.status_code))
    try:
        _commonlib_log(str(result.json()))
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
            if a < __retry_time - 1:
                _commonlib_log("retry put request time:" + str(a + 1))
                continue
            else:
                raise e
        except Exception as e:
            msg = traceback.format_exc()
            if str(msg).__contains__("[WinError 10060]"):
                if a < __retry_time - 1:
                    _commonlib_log("retry put request time:" + str(a + 1))
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
    _commonlib_log("--->http request delete :" + str(url))
    if "json" in kwargs:
        result = requests.delete(url, allow_redirects=False, verify=False, **kwargs)
    else:
        result = requests.delete(url, json=param, allow_redirects=False, verify=False, **kwargs)
    result.raise_for_status()
    _commonlib_log("<---response " + str(result.status_code))
    try:
        _commonlib_log(str(result.json()))
    except JSONDecodeError:
        pass
    return result


if __name__ == '__main__':
    param = {
        # "pwd": "$2a$10$MJHxH9MVcgGGa8UnclZKmeeSEwssfMraFZeiim7084nI2QmqNtxBC",
        "pwd": "$2a$10$9SWj8zwezzbc6qVqbK72VeDbSjf44IxNmjOZ9l1gH0WzSfMhzzx.C",
        "timestamp": int(round(time.time() * 1000)),
        "userName": "l1h"
    }
    header = {'Content-Type': 'application/json'}
    tmp_result = post("https://172.28.135.70:8443/rcdc/rco/admin/loginAdmin", param, headers=header)
    # print(result)
    cookies = tmp_result.cookies["JSESSIONID"]
    # print(cookies)
    param = {"id": "c6cd969b-d1c6-4416-b05e-dc13cf9072af"}
    # cookies = "9669AEA76ED04B65562F0860778F4249"
    tmp_result = post("https://172.28.135.70:8443/rcdc/rco/user/cloudDesktop/getInfo", data=json.dumps(param),
                      headers=header, cookies={'JSESSIONID': cookies})
    print(tmp_result)
    cookies = tmp_result.cookies["JSESSIONID"]
    print(cookies)
    # aa = {'content': {'configIp': None, 'cpu': 4, 'createTime': 1572414772598, 'desktopImageId': '481c5add-d065-40b1-bff8-f02fa22249ba', 'desktopImageName': 'hello', 'desktopImageType': 'WIN_7_64', 'desktopIp': '172.28.135.80', 'desktopMac': 'fa:16:3e:3c:3e:43', 'desktopName': 'ljt', 'desktopNetworkId': 'cadafb9b-d969-400d-80d6-330228c30672', 'desktopNetworkName': 'ruijie_autotest', 'desktopRole': 'NORMAL', 'desktopState': 'RUNNING', 'desktopStrategyId': 'b9a3d9ad-96f6-444b-b7b6-0115bf2620ec', 'desktopStrategyName': '开发', 'desktopType': 'PERSONAL', 'id': 'c6cd969b-d1c6-4416-b05e-dc13cf9072af', 'isWindowsOsActive': False, 'lastOnlineTime': None, 'latestLoginTime': 1575456250164, 'memory': 6, 'personDisk': 60, 'physicalServerIp': '172.28.31.227', 'serverName': 'rcos01', 'systemDisk': 40, 'terminalGroupName': None, 'terminalGroupNameArr': None, 'terminalId': None, 'terminalIp': None, 'terminalMac': None, 'terminalName': None, 'terminalPlatform': None, 'userCreateTime': 1572414645690, 'userGroupName': '软件兼容性工具开发', 'userGroupNameArr': ['软件兼容性工具开发'], 'userId': 'b616a937-f480-4799-a08d-bb16c2c9afd5', 'userName': 'ljt', 'userRealName': '别删', 'userType': 'NORMAL'}, 'message': None, 'msgArgArr': None, 'msgKey': None, 'status': 'SUCCESS'}
    # print(json.dumps(aa))
