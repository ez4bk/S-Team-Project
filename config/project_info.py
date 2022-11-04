import os

current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)
temp_src_dir = os.path.dirname(current_dir)
print(temp_src_dir)
if temp_src_dir.__contains__('source'):
    root_dir = os.path.dirname(temp_src_dir)
else:
    root_dir = temp_src_dir

ROOT_DIR = root_dir
LOG_DIR = os.path.join(ROOT_DIR, 'log')
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'download')

# if __name__ == '__main__':
#     pass
