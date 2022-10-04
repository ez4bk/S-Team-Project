# coding=utf-8

from lib.commonlib.base_lib.network import http_request


def open_authorize(server_ip, cookies, timeout=480):
    """
    :param timeout:
    :param server_ip:
    :param cookies:
    :return:
    """
    header = {'Content-Type': 'text/html'}
    url = 'https://' + server_ip + '/web/provisionalAuthorization/openAuthorize'
    result = http_request.post(url, data=str(timeout), headers=header, cookies={'JSESSIONID': cookies})
    re = result.json()
    return re['code'] == 0, re


if __name__ == '__main__':
    open_authorize("172.28.76.251", "D98A0EAE35AF0B4910A799C7523198A4", 480)
