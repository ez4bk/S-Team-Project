# coding=utf-8
import os
import traceback

import paramiko

from config.project_info import DOWNLOAD_DIR, VM_SRC_DIR
from lib.base_lib.mylog.mylog import _commonlib_log, _commonlib_log_e
from lib.base_lib.sftp_utils.ftp_info import FtpInfo


class SftpUtils(object):
    """
    SFTP 工具类，可以实现通过sftp协议进行本地与远程sftp服务端的文件上传与下载。

    示例代码如下::

        tmp_ftp_info = FtpInfo("172.28.100.133", 9622, "root", "MDE5MZTJjZTY1")
        aa = SftpUtils(tmp_ftp_info)
        tmp_result = aa.sftp_upload("D:\\aa.txt", "/opt/aa.txt")
        print(tmp_result)

    """

    def __init__(self, ftp_info=FtpInfo()):
        self.__ftp_info = ftp_info

    def sftp_upload(self, local_file, remote_file):
        """
        上传文件到服务端。需要注意的是，当remote_file中的文件夹不存在是，将会上传失败，需要调用:py:func:`mkdirs`.进行文件夹创建。
        同时，remote_file为要上传到服务端的文件名，不是文件夹路径。如：sftp_upload("D:\\abc.txt","/ftp/backup/abc.txt")

        :param local_file: 要上传的本地文件名
        :param remote_file: 服务端文件保存名称，不可为文件路径文件夹

        :return: 返回上传的结果，类型为bool
        """
        for a in range(3):
            remote_path = VM_SRC_DIR + '/' + remote_path
            flag = self.__sftp_upload(self.__ftp_info, local_file, remote_file)
            if flag:
                return True
        return False

    @staticmethod
    def __sftp_upload(ftp_info, local_file, remote_file):
        """
        :type ftp_info SshInfo
        :param ftp_info:
        :param local_file:
        :param remote_file:
        :return:
        """
        _commonlib_log("sftp_upload(" + str(ftp_info) + "," + str(local_file) + "," + str(remote_file) + ")")
        scp = None
        try:
            scp = paramiko.Transport((ftp_info.ip, ftp_info.port))
            scp.connect(username=ftp_info.user_name, password=ftp_info.user_password)
            sftp = paramiko.SFTPClient.from_transport(scp)
            sftp.put(local_file, remote_file)
            scp.close()
        except:
            _commonlib_log_e(traceback.format_exc())
            if scp is not None:
                scp.close()
            return False
        return True

    def sftp_download(self, remote_file, local_file):
        """
        从sftp服务端下载文件到本地。需要注意的是，当local_file中的文件夹不存在是，将会下载失败，需要调用自行创建本地文件夹。
        同时，local_file为要下载到本地的文件名，不是文件夹路径。如：sftp_upload("/ftp/backup/abc.txt","D:\\backup\\abc.txt")

        :param remote_file: 要下载的远程文件名称
        :param local_file:  本地保存的文件名称

        :return:    返回下载结果
        """
        for a in range(3):
            local_path = os.path.join(DOWNLOAD_DIR, local_file)
            flag = self.__sftp_download(self.__ftp_info, remote_file, local_path)
            if flag:
                return True
        return False

    @staticmethod
    def __sftp_download(ftp_info, remote_file, local_file):
        """
        :type ftp_info FtpInfo
        :param ftp_info:
        :param remote_file:
        :param local_file:
        :return:
        """
        _commonlib_log("download_file_from_server(" + str(remote_file) + "," + local_file + ")")
        scp = None
        try:
            scp = paramiko.Transport((ftp_info.ip, ftp_info.port))
            scp.connect(username=ftp_info.user_name, password=ftp_info.user_password)
            sftp = paramiko.SFTPClient.from_transport(scp)
            sftp.get(remote_file, local_file)
            scp.close()
        except:
            _commonlib_log_e(traceback.format_exc())
            if scp is not None:
                scp.close()
            return False
        return True

    def mkdirs(self, remote_path):
        """
        在ftp服务端创建文件夹，支持多层组同时创建，如 /ftp/project/data, 当服务端无此文件夹时，将按层级依次创建ftp、project、data文件夹

        :param remote_path: 要创建的文件路径

        :return:    文件夹创建结果，类型为bool

        """
        scp = None
        try:
            scp = paramiko.Transport((self.__ftp_info.ip, self.__ftp_info.port))
            scp.connect(username=self.__ftp_info.user_name, password=self.__ftp_info.user_password)
            sftp = paramiko.SFTPClient.from_transport(scp)
            path_name_list = str(remote_path).split("/")
            tmp = ""
            for a in range(len(path_name_list)):
                tmp += (path_name_list[a] + "/")
                try:
                    sftp.chdir(tmp)
                except:
                    _commonlib_log_e(traceback.format_exc())
                    sftp.mkdir(tmp)
            scp.close()
        except:
            _commonlib_log_e(traceback.format_exc())
            if scp is not None:
                scp.close()
            return False
        return True

    def upload(self, local_file, remote_file):
        t = paramiko.Transport((self.__ftp_info.ip, self.__ftp_info.port))
        t.connect(username=self.__ftp_info.user_name, password=self.__ftp_info.user_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        # sftp.put(local_image_path, remote_image_path)
        # t.close()

        # 断点续传方案
        file_list = sftp.listdir(os.path.dirname(remote_file))

        if remote_file in file_list:
            stat = sftp.stat(remote_file)
            with open(local_file, mode='rb') as f_local:
                f_local.seek(stat.st_size)
                f_remote = sftp.open(remote_file, "a")
                f_remote.set_pipelined(True)
                while True:
                    tmp_buffer = f_local.read(32768)
                    if len(tmp_buffer) == 0:
                        break
                    f_remote.write(tmp_buffer)
                f_remote.close()
        else:
            with open(local_file, mode='rb') as f_local:
                f_remote = sftp.open(remote_file, "w")
                f_remote.set_pipelined(True)
                while True:
                    tmp_buffer = f_local.read(32768)
                    if len(tmp_buffer) == 0:
                        break
                    f_remote.write(tmp_buffer)
                f_remote.close()


if __name__ == '__main__':
    # tmp_ftp_info = FtpInfo("172.28.100.133", 9622, "root", "MDE5MZTJjZTY1")
    aa = SftpUtils()
    tmp_result = aa.sftp_download(VM_SRC_DIR + "/snake.py", 'sftp_game.py')
    print(tmp_result)
    # aa.mkdirs(tmp_ftp_info, "/opt/aaa/bbb")
