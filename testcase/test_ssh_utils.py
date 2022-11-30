import os

from config.project_info import DOWNLOAD_DIR, VM_SRC_DIR
from lib.base_lib.ssh.ssh_utils import SshUtils

ssh_utils = SshUtils()
HELLO_WORLD = 'Hello World'


class TestSshUtils(object):
    def test_get_ssh_info(self):
        ssh_info = ssh_utils.get_ssh_info()
        assert ssh_info is not None
        assert ssh_info.ip == 'cs431-06.cs.rutgers.edu'
        assert ssh_info.port == 22
        assert ssh_info.user_name == 'yw780'
        assert ssh_info.user_pwd == 'Wyc1qaz2wsx~'

    def test_check_ssh(self):
        assert ssh_utils.check_ssh()

    def test_exec_command(self):
        cmd = 'echo "%s"' % HELLO_WORLD
        assert ssh_utils.exec_command(cmd) == HELLO_WORLD

    def test_download_from_ssh(self):
        test_file_name = 'test_download_from_ssh.txt'
        test_file_rename = 'test_download_from_ssh_rename.txt'
        test_file_vm_path = VM_SRC_DIR + '/' + test_file_name
        test_file_local_path = os.path.join(DOWNLOAD_DIR, test_file_name)
        test_file_rename_local_path = os.path.join(DOWNLOAD_DIR, test_file_rename)

        # shutil.rmtree(DOWNLOAD_DIR)
        try:
            os.mkdir(DOWNLOAD_DIR)
        except OSError as e:
            pass

        new_file_cmd = 'echo "{0}" >> {1}'.format(HELLO_WORLD, test_file_vm_path)
        ssh_utils.exec_command(new_file_cmd)

        ssh_utils.download_from_ssh(test_file_vm_path, test_file_name)
        ssh_utils.download_from_ssh(test_file_vm_path, test_file_rename)

        for root, dirs, files in os.walk(DOWNLOAD_DIR):
            assert test_file_name in files
            assert test_file_rename in files

        f = open(test_file_local_path, 'r')
        f_r = open(test_file_rename_local_path, 'r')
        assert f.read().strip('\n') == HELLO_WORLD
        assert f_r.read().strip('\n') == HELLO_WORLD
        f.close()
        f_r.close()

        delete_file_cmd = 'rm {}'.format(test_file_vm_path)
        ssh_utils.exec_command(delete_file_cmd)
        os.remove(test_file_local_path)
        os.remove(test_file_rename_local_path)
