# -*- coding: cp936 -*-
import os
import sys


# 获取脚本文件的当前路径
def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return str(path)
    elif os.path.isfile(path):
        return str(os.path.dirname(path))


# 打印结果
if __name__ == '__main__':
    # print(cur_file_dir())
    path = os.getcwd()
    print(path)
    os.chdir('..')
    path = os.getcwd()
    print(path)
