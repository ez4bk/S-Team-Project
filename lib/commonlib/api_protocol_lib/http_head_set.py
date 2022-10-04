#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2019/11/27 18:41
"""
import json
import time
import traceback

import requests
import bcrypt
from commonlib.base_lib.mylog.mylog import log

from commonlib.base_lib.ssh.server_ssh import ServerSsh
from commonlib.base_lib.utils.aes_pass import AESCipher

requests.packages.urllib3.disable_warnings()

SUNNY_VERSION = 2.1
TIMEZONE_OFFSET = 8
CLIENT_TYPE = 'windows_client'
SUNNY_DATA_PORT = '9000'
HTTPS_CONTENT_TYPE = 'application/json'

encrypt_type = "new"


def get_sunny_user_pwd_encode(server_ip, password, ssh_info, encode_file_path='/usr/rcd/bin/aes_encode.sh'):
    # 测试数 port=22, user_name='rcdtest', user_pwd='b9594546', root_name='rcdtest', root_pwd='b9594546'
    # ssh_info = SshInfo(server_ip, gvalue.TERMINAL_SSH_PORT, gvalue.SERVER_SSH_USER, gvalue.server_ssh_password,
    #                    "root", gvalue.server_ssh_password)
    ssh = ServerSsh(server_ip, ssh_info)
    pwd_encode = ssh.exec_command('sh {0} {1}'.format(encode_file_path, password))
    return pwd_encode.strip()


def php_head_set(server_ip, sunny_user, sunny_user_password, login_api_name='/rj/index.php',
                 init_api_name='/rj/index.php/apps/files/initial.php', ssh_info=None, encode_file_path=None, **kwargs):
    pwd = get_sunny_user_pwd_encode(server_ip, sunny_user_password, ssh_info=ssh_info,
                                    encode_file_path=encode_file_path)
    if 'data' not in kwargs:
        data = dict()
        data['user'] = sunny_user
        data['version'] = SUNNY_VERSION
        data['timezone-offset'] = TIMEZONE_OFFSET
        data['type'] = CLIENT_TYPE
        data['password'] = pwd
    else:
        data = kwargs['data']
    head_info_dic = dict()
    result = requests.post('http://{0}:{1}{2}'.format(server_ip, SUNNY_DATA_PORT, login_api_name),
                           data=data, allow_redirects=False, verify=False)
    if result.status_code == 302:
        res = result.headers
        info = res['Set-Cookie'].split('; ')
        head_info_dic['cookie'] = info[0]
        result2 = requests.get('http://{0}:{1}{2}'.format(server_ip, SUNNY_DATA_PORT, init_api_name),
                               cookies=result.cookies, allow_redirects=False, verify=False)
        if result2.json()["status"] == 'success':
            head_info_dic['requesttoken'] = (result2.json()["data"]["requesttoken"])
        else:
            log(" user {} initial fail".format(sunny_user))
    else:
        log("user {} login fail ".format(sunny_user))
    return head_info_dic


def http_get_cookie(login_url, user_name, user_pwd):
    global encrypt_type
    try:
        cookies = _http_get_cookie_do(login_url, user_name, user_pwd, encrypt_type)
        if type(cookies) is tuple:
            if encrypt_type == "new":
                tmp = "old"
            else:
                tmp = "new"
            encrypt_type = tmp
            cookies = _http_get_cookie_do(login_url, user_name, user_pwd, tmp)
    except Exception:
        if encrypt_type == "new":
            tmp = "old"
        else:
            tmp = "new"
        encrypt_type = tmp
        cookies = _http_get_cookie_do(login_url, user_name, user_pwd, tmp)
        if type(cookies) is tuple:
            assert False,cookies[1]
    return cookies


def _http_get_cookie_do(login_url, user_name, user_pwd, encrypt="new"):
    log("http_get_cookie(" + str(login_url) + "," + str(user_name) + "," + user_pwd + ")")
    if encrypt == "new":
        e = AESCipher(key="ADMINPASSWORDKEY")
        encode_pwd = e.encrypt_main(user_pwd)
    else:
        encode_pwd = (bcrypt.hashpw(user_pwd.encode('utf-8'), bcrypt.gensalt(prefix=b'2a')).decode('utf-8'))
    data = dict()
    data['userName'] = user_name
    data['pwd'] = encode_pwd
    data['timestamp'] = round(time.time() * 1000)
    data['autoRefresh'] = False
    headers = base_head_info()
    try:
        result = requests.post(login_url, data=json.dumps(data), headers=headers, allow_redirects=False, verify=False)
    except Exception:
        log(traceback.format_exc())
        print(traceback.format_exc())
        return False, f"can not login {login_url} with {user_name}/{user_pwd}"
    assert result.status_code == 200
    response = result.json()
    log(response)
    if response["status"] != "SUCCESS":
        raise Exception("can not get cookies")
    global encrypt_type
    encrypt_type = encrypt
    head = result.headers
    info = head['Set-Cookie'].split('; ')
    return info[0]


def base_head_info(content_type=HTTPS_CONTENT_TYPE):
    headers = dict()
    headers['content-type'] = content_type
    return headers


def https_dead_set(cookie_type=0, login_url=None, user_name=None, user_pwd=None):
    headers = base_head_info()
    if cookie_type == 0:
        cookie = http_get_cookie(login_url, user_name, user_pwd, )
        headers['cookie'] = cookie
    return headers


def pwd_encode(user_pwd):
    encode_pwd = (bcrypt.hashpw(user_pwd.encode('utf-8'), bcrypt.gensalt(prefix=b'2a')).decode('utf-8'))
    return encode_pwd


# def sunny_encryt_encod(pwd, key):
#     while len(pwd) % 16 != 0:
#         pwd += (16 - len(pwd) % 16) * chr(16 - len(pwd) % 16)
#     while len(key) % 16 != 0:
#         key += (16 - len(key) % 16) * chr(16 - len(key) % 16)
#     data = str.encode(pwd)
#     key_bytes = bytes(key, encoding='utf-8')
#     aes = AES.new(key_bytes, AES.MODE_CBC)
#     return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')


if __name__ == "__main__":
    pass
    # result3 =requests.post('https://172.28.110.40:5000/restful', headers=heads, data=data3,)
    # result3 = http_get_cookie('https://172.28.135.70:8443/rcdc/rco/admin/loginAdmin', 'admin', 'rcos2019')
    # print(result3)
    # get_sunny_cookie('https://172.28.100.159:9270/rj/index.php', 'admin', 'admin123')
