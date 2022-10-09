import os
import zipfile

from lib.base_lib.mylog.mylog import _commonlib_log


def zip_extract(source_zip_file, target_path):
    """
    解压缩文件

    :param source_zip_file: zip文件名
    :param target_path:     要解压到的目录
    """
    z = zipfile.ZipFile(source_zip_file, 'r')
    _commonlib_log("zip extract from " + os.path.abspath(source_zip_file) + " to " + os.path.abspath(target_path))
    z.extractall(path=target_path)
    z.close()


def zip_file(source_file_name, zip_file_name):
    """
    压缩文件或文件夹

    :param source_file_name: 要压缩的文件名
    :param zip_file_name:   压缩后的文件名称

    """
    zf = zipfile.ZipFile(zip_file_name, "w", zipfile.zlib.DEFLATED)
    zf.write(source_file_name, os.path.basename(source_file_name))
    zf.close()


if __name__ == '__main__':
    # path = r"C:\Users\R10707\Desktop\mysql-5.7.22-winx64.zip"
    # zip_extract(path, os.path.dirname(path))
    zip_file(r"D:\SVN\TypicalTest\mylog\2019-08-12.mylog", r"D:\SVN\TypicalTest\log\2019-08-12.zip")
