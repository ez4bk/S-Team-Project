import os

current_dir = os.path.dirname(os.path.realpath(__file__))
temp_src_dir = os.path.dirname(current_dir)
if temp_src_dir.__contains__('source'):
    root_dir = os.path.dirname(temp_src_dir)
else:
    root_dir = temp_src_dir

ROOT_DIR = root_dir
LOG_DIR = os.path.join(ROOT_DIR, 'log')
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'download')
try:
    os.mkdir(DOWNLOAD_DIR)
except OSError as e:
    pass

VM_SRC_DIR = "/home/famiowl_files"
