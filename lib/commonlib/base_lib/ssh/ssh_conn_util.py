#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2019/12/19 17:30
"""
import os
import re
import time

import paramiko
from lib.commonlib.base_lib.ssh.server_ssh import ServerSsh

from lib.commonlib.base_lib.mylog.mylog import log, log_e
from lib.commonlib.base_lib.ssh.ssh_info import SshInfo


# from source.common_func.common_fun import get_time_stamp


def cmd_exec_result_wait(chan, cmd, timeout=8 * 1000, wait_type=0, wait_time=1, search_time=0.5):
    log('<<<<<<<<<<<<execute cmd %s ' % cmd)
    chan.send(cmd + '\n')
    buff = ''
    chan.settimeout(timeout / 1000 + 2)
    while True:
        return get_result(chan, cmd, wait_type=wait_type, buff=buff, wait_time=wait_time, search_time=search_time)


def get_result(chan, cmd, wait_type=0, buff='', wait_time=1, search_time=0.5):
    import select
    chan.setblocking(False)
    time.sleep(1)
    for i in range(wait_time):
        select.select([chan], [], [], 600)
        resp = chan.recv(9999).decode('utf8')
        buff += str(resp).replace(' \r', '').replace('\r', '')
        if buff.endswith('# ') or buff.endswith("$ ") or buff.__contains__('logout') or buff.__contains__(']#'):
            log('get result %s' % buff)
            buff = buff.strip()
            buff = buff.replace(cmd, '')
            buff = buff.replace(']0', '').strip()
            end_list = re.findall(r'\[root@.*?\]#', buff)
            end_list1 = re.findall(r'root@.*?#', buff)
            docker_end_list = re.findall(r';@.*?\[root@.*?\]#', buff)
            end_list = docker_end_list + end_list + end_list1
            if end_list:
                for item in end_list:
                    buff = buff.replace(item, '')
                    return buff.strip()
        else:
            time.sleep(search_time)
            # log("get result time more than %s second,result is %s " % (search_time, buff))
            if wait_type != 0:
                return buff.strip()
    log("result is %s " % buff)
    return buff


def result_deal(result):
    """
    去除颜色
    :param result:
    :return:
    """
    if result:
        result = re.sub(r"\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]", "", result)
    return result


# def terminal_download_conn(ip, dir_path, file_name, local_dir=download_picture_dir, os_type="idv_shine"):
#     log(f"连接终端下载文件")
#     for i in range(3):
#         try:
#             scp = paramiko.Transport((ip, ssh_info.get(os_type).get('port')))
#             scp.connect(username=ssh_info.get(os_type).get('user'), password=ssh_info.get(os_type).get('pwd'))
#             # file_name = dir_path.rsplit('/', 1)[1]
#             sftp = paramiko.SFTPClient.from_transport(scp)
#             # files = sftp.listdir(dir_path)
#             # for f in files:
#             # sftp.get(os.path.join(dir_path, f), os.path.join(local_dit, f))
#             path = os.path.join(local_dir, get_time_stamp() + file_name)
#             sftp.get(dir_path, path)
#
#             # log(u"-----%s下载终端文件到本地，路径为：%s---------" % (ip, path))
#             scp.close()
#             return path
#         except Exception as e:
#             if i == 2:
#                 raise e
#             log_e(e)
#             time.sleep(2)
#             log_e(u"-------连接终端%s下载文件失败再次尝试------" % ip)


# def terminal_upload_conn(ip, file_name, local_path=os.getcwd(), remote_path="/root/", os_type="idv_shine"):
#     """连接终端上传文件"""
#     for i in range(3):
#         try:
#             scp = paramiko.Transport((ip, ssh_info.get(os_type).get('port')))
#             scp.connect(username=ssh_info.get(os_type).get('user'), password=ssh_info.get(os_type).get('pwd'))
#             sftp = paramiko.SFTPClient.from_transport(scp)
#             local_file = os.path.join(local_path, file_name)
#             remote_file = os.path.join(remote_path, file_name)
#             sftp.put(local_file, remote_file)
#             scp.close()
#         except Exception as e:
#             if i == 2:
#                 raise e
#             log_e(e)
#             time.sleep(2)
#             log_e(u"-------连接服务器%s上传文件失败再次尝试------" % ip)


def terminal_operate(server_ip, cmd, time_sleep=0):
    """
    通过cmd命令完成终端操作(终端可以是ivd shine，可以是裸刷VDI，也可以是IDV云桌面，或者VDI云桌面)
    :param server_ip:终端IP,裸刷虚机IP，或者云桌面IP
    :param cmd:指令
    :param time_sleep

    :return:
    """
    ssh = SshConn(server_ip=server_ip,
                  port=ssh_info.get(os_type).get('port'),
                  user=ssh_info.get(os_type).get('user'),
                  pwd=ssh_info.get(os_type).get('pwd'),
                  root_pwd=ssh_info.get(os_type).get('root_pwd'),
                  os_type=os_type)
    res = ssh.shell_command(server_ip, cmd)
    time.sleep(time_sleep)
    return res


def terminal_operate_without_response(server_ip, cmd, os_type="idv_shine", time_sleep=0):
    ssh = SshConn(server_ip=server_ip,
                  port=ssh_info.get(os_type).get('port'),
                  user=ssh_info.get(os_type).get('user'),
                  pwd=ssh_info.get(os_type).get('pwd'),
                  root_pwd=ssh_info.get(os_type).get('root_pwd'),
                  os_type=os_type)
    ssh.shell_command_no_response(server_ip, cmd)
    time.sleep(time_sleep)


def terminal_screen(server_ip, os_type="idv_shine"):
    """
    idv终端截屏
    :param server_ip:终端IP
    :param os_type
    :return:
    """
    picture_dir = 'Pictures'
    cmd = 'export DISPLAY=:0;mkdir {0};rm {0}/set.png;scrot ~/{0}/set.png'.format(picture_dir)
    terminal_operate(server_ip, cmd, os_type=os_type)
    # log(u"-----%s终端截屏---------" % (cmd))
    return picture_dir + '/set.png'


def download_terminal_screen(server_ip, local_dir=download_picture_dir, os_type="idv_shine"):
    """
    idv终端下载截屏文件
    :param server_ip:
    :param local_dir:
    :param os_type:
    :return:
    """
    path = terminal_screen(server_ip, os_type)
    file_name = os.path.basename(path)
    local_path = terminal_download_conn(server_ip, dir_path=path, local_dir=local_dir, file_name=file_name)
    log(u"-----%s下载截屏文件：%s---------" % (server_ip, local_path))
    return local_path


def ssh_check(ip, os_type, times=5, sleep_time=5):
    assert len(ip) is not 0, log_e("ssh连接错误，ip为空！")
    ssh_no_error = SshConn(
        server_ip=ip, port=ssh_info.get(os_type).get('port'), user=ssh_info.get(os_type).get('user'),
        pwd=ssh_info.get(os_type).get('pwd'), root_pwd=ssh_info.get(os_type).get('root_pwd'), os_type=os_type)
    for i in range(times):
        log("确保云桌面ssh服务已启动，第%d次尝试" % i)
        res = ssh_no_error.shell_command_no_error(ip, 'pwd')
        if res is not None:
            if len(res) is not 0:
                time.sleep(sleep_time)
                return
        else:
            time.sleep(2)


def wget_file_from_http(ip, os_type, http_link, remote_path='~', time_sleep=0):
    if '172.17.83.11' in http_link:
        http_link = http_link.split('http://')[1]
        http_link = 'http://share:share@' + http_link
    terminal_operate(ip, 'wget {} -P {}'.format(http_link, remote_path), os_type, time_sleep)


class SshConn(ServerSsh):
    def __init__(self, server_ip=SERVER_VIP, port=RCDC_SERVER_PORT, user=RCDC_SERVER_USER, pwd=RCDC_SERVER_PWD,
                 root_pwd=RCDC_SERVER_PWD, os_type="idv_shine"):
        self.server_ip = server_ip
        self.server_port = port
        self.server_user = user
        self.server_pwd = pwd
        self.root_pwd = root_pwd
        self.os_type = os_type
        self.ssh_info = SshInfo(self.server_ip, self.server_port, self.server_user, self.server_pwd,
                                "root", self.root_pwd)
        ServerSsh.__init__(self, device_ip=server_ip, ssh_info=self.ssh_info)

    def ssh_conn(self, ip, timeout=8):
        for a in range(3):
            try:
                log(f">>>>>>>>>>>>>>>>> {ip} {self.server_port} {self.server_user} {self.server_pwd} {self.root_pwd} {self.os_type}")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=self.server_port, username=self.server_user, password=self.server_pwd,
                            timeout=timeout)
                return ssh
            except Exception as e:
                log(f"{e}, {ip}, {self.server_port}, {self.server_user}, {self.server_pwd}")
                log("<<<<<<<<<<<<<<<<<<{} ssh connect fail<<<<<<".format(ip))

    def shell_command(self, ip, command, timeout=8):
        """连接服务器"""
        for i in range(3):
            ssh = self.ssh_conn(ip, timeout=timeout)
            try:
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=False)
                result = stdout.read()
                log(f"ssh_command >>> 执行命令是'{command}'\t执行命令结果是'{bytes.decode(result)}'")
                ssh.close()
                return bytes.decode(result)
            except Exception as e:
                time.sleep(3)
                log_e(f"服务器{ip}连接失败,失败原因是{e}")
                ssh.close()

    def shell_command_no_response(self, ip, command, timeout=8):
        """连接服务器"""
        for i in range(3):
            ssh = self.ssh_conn(ip, timeout=timeout)
            try:
                ssh.exec_command(command, get_pty=False)
                ssh.close()
                return
            except Exception as e:
                time.sleep(3)
                log_e(f"服务器{ip}连接失败,失败原因是{e}")
                ssh.close()

    def shell_command_no_error(self, ip, command, timeout=8):
        """连接服务器"""
        for i in range(3):
            ssh = self.ssh_conn(ip, timeout=timeout)
            try:
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=False)
                result = stdout.read()
                log(f"ssh_command >>> 执行命令是'{command}'\t执行命令结果是'{result}'")
                ssh.close()
                return bytes.decode(result)
            except Exception as e:
                time.sleep(3)
                log_e(f"服务器{ip}连接失败,失败原因是{e}")

    def change_to_root_shell_command(self, cmd, cmd_timeout=10 * 1000, wait_type=0):
        if self.ssh_conn(self.server_ip):
            self._ssh_client = self.ssh_conn(self.server_ip)
            log("server ssh cmd: " + str(cmd))
            chanel_ssh_ob = self._ssh_client.invoke_shell()  # 建立交互式的shell
            chanel_ssh_ob.settimeout(cmd_timeout / 1000 + 3)  # 设置接收与发送超时时间
            result = self._chanel_root(chanel_ssh_ob, self._ssh_info.root_pwd)
            if result:
                try:
                    temp_result = cmd_exec_result_wait(chanel_ssh_ob, cmd, wait_type=wait_type)
                    final_result = result_deal(temp_result)
                    return chanel_ssh_ob, final_result
                except Exception as e:
                    chanel_ssh_ob.close()
                    log_e('<<<<<<<<<shell 连接执行%s指令报错' % cmd)
                    log_e(e)
        else:
            log_e('<<<<<<<<连接服务器失败')
            raise ConnectionAbortedError

    def shell_exec_cmd(self, ip, cmd):
        tmp_client = ServerSsh(device_ip=ip, ssh_info=self.ssh_info)
        return tmp_client.exec_command(cmd)

    def scp_file(self, local_file, remote_server, remote_file, remote_port=RCDC_SERVER_PORT,
                 remote_pwd=RCDC_SERVER_PWD, time_out=30):
        scp_cmd = 'rm -f  /root/.ssh/known_hosts;scp -P {0} {1} root@{2}:{3} '.format(remote_port, local_file,
                                                                                      remote_server, remote_file)
        # 清除密钥过期方法rm -f  /root/.ssh/known_hosts;
        chan, result = self.change_to_root_shell_command(scp_cmd, cmd_timeout=8 * 1000, wait_type=1)
        if result.lower().__contains__('(yes/no)?'):
            result = cmd_exec_result_wait(chan, 'yes', 2 * 1000, wait_type=1)
        if result.lower().__contains__('password'):
            chan.send(remote_pwd + '\n')
        t = time.time()
        for i in range(time_out):
            result = get_result(chan, remote_pwd, wait_type=0, buff='')
            if result.__contains__('No such file or directory'):
                return result
            elif result.__contains__('100%'):
                return result
            else:
                time.sleep(1)
                t1 = time.time()
                if t1 - t > time_out:
                    log("传输文件时间超时，超过{0}秒".format(time_out))
                    return result


if __name__ == '__main__':
    wget_file_from_http('172.17.81.233', 'physical_machine',
                        'http://172.17.83.11:8080/E%3A/data/04-%E6%B5%8B%E8%AF%95%E7%BB%84/01%20%E5%B8%B8%E7%94%A8%E8%BD%AF%E4%BB%B6/%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85%E5%8C%85/04%20%E8%87%AA%E5%8A%A8%E5%8C%96%E8%84%9A%E6%9C%AC%E9%9C%80%E8%A6%81%E7%9A%84%E8%BD%AF%E4%BB%B6%E5%8C%85/app_distribute/test_audio.mp3')
