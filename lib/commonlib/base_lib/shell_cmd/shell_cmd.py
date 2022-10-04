import os
import re
import traceback

import paramiko

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log, _commonlib_log_e
from lib.commonlib.base_lib.ssh.server_ssh import ServerSsh
from lib.commonlib.base_lib.ssh.terminal_ssh import TerminalSsh

ONE_K_SIZE = 1024
ONE_M_SIZE = 1024 * 1024
ONE_G_SIZE = 1024 * 1024 * 1024  # 1024*1024*1024


def scp_file(ssh_client, scp_cmd, password, timeout=30 * 1000):
    def process_func(channel, msg):
        print(msg)
        if str(msg).endswith("(yes/no)? "):
            channel.send('yes\n')
        if str(msg).endswith("password: "):
            channel.send(f'{password}\n')

    ssh_client.exec_command("rm -f  /root/.ssh/known_hosts;")
    result = ssh_client.channel_exec_command(cmd=scp_cmd, cmd_timeout=timeout, process_callback=process_func)
    return result


def sftp_upload(ssh_info, local_file, remote_file):
    """
    :type ssh_info SshInfo
    :param ssh_info:
    :param local_file:
    :param remote_file:
    :return:
    """
    _commonlib_log("sftp_upload(" + str(ssh_info) + "," + str(local_file) + "," + str(remote_file) + ")")
    scp = paramiko.Transport((ssh_info.ip, ssh_info.port))
    scp.connect(username=ssh_info.user_name, password=ssh_info.user_pwd)
    sftp = paramiko.SFTPClient.from_transport(scp)
    sftp.put(local_file, remote_file)
    scp.close()
    return True


def download_file_from_server(ssh_info, remote_file, local_file):
    """
    :type ssh_info SshInfo
    :param ssh_info:
    :param remote_file:
    :param local_file:
    :return:
    """
    _commonlib_log("download_file_from_server(" + str(remote_file) + "," + local_file + ")")
    scp = None
    try:
        scp = paramiko.Transport((ssh_info.ip, ssh_info.port))
        scp.connect(username=ssh_info.user_name, password=ssh_info.user_pwd)
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.get(remote_file, local_file)
        scp.close()
    except:
        _commonlib_log(traceback.format_exc())
        if scp is not None:
            scp.close()
        return False
    return True


def take_terminal_screen_cap(ssh_client, pic_path, picture_name):
    picture_name = os.path.basename(picture_name)
    ssh_client.exec_command("mkdir " + pic_path)
    ssh_client.exec_command(
        "export DISPLAY=:0;sleep 0.15;rm " + pic_path + "/" + str(
            picture_name) + ";sleep 0.15;scrot " + pic_path + "/" + str(
            picture_name))


def terminal_reboot_ssh(terminal_ip):
    _commonlib_log("reboot terminal ip " + str(terminal_ip))
    # terminal_request.reboot_terminal(ip, cookies, terminal_id)
    ssh_client = TerminalSsh(terminal_ip)
    ssh_client.exec_command("sync")
    ssh_client.exec_command("sync")
    ssh_client.exec_command("reboot")


def get_linux_product_name(ssh_client):
    msg = ssh_client.exec_command('dmidecode | grep "Product Name"')
    msg = re.findall(r"Product Name.*: (.*)", msg)
    _commonlib_log("terminal product name is " + str(msg))
    return str(msg[0]).strip(), str(msg[1]).strip()


def reboot_server(server_ip):
    """
    重启服务器，此接口为同步接口。鉴于对实际服务器重启操作的执行，预计在1分钟内返回，因此设置reboot_server超时返回时间为60S。reboot_server后，需要调用server_ssh.check_ssh()接口校验连接状态

    :param server_ip: 要进行重启的服务器IP地址
    """
    _commonlib_log("reboot server " + server_ip)
    ssh_client = ServerSsh(server_ip)
    ssh_client.exec_command("reboot -fn", 60 * 1000)


def exec_cmd(server_ip, cmd, tms=5):
    """执行ssh 命令"""
    ssh_client = ServerSsh(server_ip)
    if ssh_client.check_ssh():
        return ssh_client.exec_command(cmd, tms)
    else:
        ssh_client = TerminalSsh(server_ip)
        if ssh_client.check_ssh():
            return ssh_client.exec_command(cmd, tms)
        else:
            raise Exception("can not ssh server " + str(server_ip))


def file_contain_(file_name):
    if file_name.__contains__("(") and not file_name.__contains__("\("):
        file_name = file_name.replace("(", "\(").replace(")", "\)")
    return file_name


def create_file(server_ip, file_path, size):
    """
    创建指定大小文件
    file_path: 文件的绝对路径
    size： 文件大小
    """
    if file_path is None or file_path == "":
        return False

    if size is 0:
        cmd = "touch " + file_path
    else:
        bs = size
        count = 1
        if size > 32 * ONE_M_SIZE:
            bs = 32 * ONE_M_SIZE
            count = size / bs
        cmd = "dd if=/dev/urandom of=%s bs=%s count=%d" % (file_path, bs, count)

    _commonlib_log("创建文件%s, size:%d" % (file_path, size))
    ret, err = exec_cmd(server_ip, cmd)
    if ret != "":
        return False
    ret, err = exec_cmd(server_ip, "sync")
    if ret != "":
        return False
    return True


def count_files(server_ip, path):
    # 检查文件夹下文件个数
    path = file_contain_(path)
    cmd = "cd " + path + "; ls -lR|grep '^-'| wc -l"
    ret = exec_cmd(server_ip, cmd)
    if ret == "":
        return None
    return int(ret)


def delete_path(server_ip, path):
    # 删除文件或目录
    path = file_contain_(path)
    cmd = "rm -rf " + path
    ret = exec_cmd(server_ip, cmd)
    if ret != "":
        _commonlib_log_e("删除文件错误 %s : stdout= %s" % (path, ret))
        return False
    else:
        return True


def is_file_exist(server_ip, path, name):
    # 查找文件是否存在
    src_name = name  # 从命令行获取的文件不带(, 输入命令行的文件必须带转义字符\（
    name = file_contain_(name)
    if not path.endswith("/") and not name.startswith("/"):
        path += "/"
    cmd = "find " + path + " -name " + name
    ret = exec_cmd(server_ip, cmd)
    if ret == "":
        return False
    file_name = path + src_name
    print("path:" + file_name)
    if ret.__contains__(file_name):
        return True
    else:
        _commonlib_log_e("未查找到文件: %s  err= %s" % (file_name, ret))
        return False


def get_server_file_md5(ip, remote_file):
    msg = exec_cmd(ip, "md5sum " + remote_file, 10 * 60 * 1000)
    _commonlib_log("get server file md5 return " + str(msg))
    if msg == "":
        return ""
    return re.findall("(\w+) ", msg)[0]


def get_file_size(server_ip, file_path):
    # 获取文件的大小
    file_path = file_contain_(file_path)

    cmd = "wc -c " + file_path + " |awk -F ' ' {'print $1'}"
    ret = exec_cmd(server_ip, cmd)
    if ret == "":
        return False
    if ret.startswith("wc:"):
        return False
    size = int(ret)
    # size = int(ret[0:ret.find(" ") + 1])
    _commonlib_log("size:%d" % size)
    return size
