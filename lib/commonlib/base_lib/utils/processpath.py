# -*- coding: cp936 -*-
import os
import sys


# ��ȡ�ű��ļ��ĵ�ǰ·��
def cur_file_dir():
    # ��ȡ�ű�·��
    path = sys.path[0]
    # �ж�Ϊ�ű��ļ�����py2exe�������ļ�������ǽű��ļ����򷵻ص��ǽű���Ŀ¼�������py2exe�������ļ����򷵻ص��Ǳ������ļ�·��
    if os.path.isdir(path):
        return str(path)
    elif os.path.isfile(path):
        return str(os.path.dirname(path))


# ��ӡ���
if __name__ == '__main__':
    # print(cur_file_dir())
    path = os.getcwd()
    print(path)
    os.chdir('..')
    path = os.getcwd()
    print(path)
