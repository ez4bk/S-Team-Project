# coding=utf-8
import re
import sys

from lib.commonlib.base_lib.system_utils.myos import MyOs

my_os = MyOs()

if str(sys.platform) == "linux":
    AND = " && "
else:
    AND = " & "


def check_diff(file_name, base_path=""):
    if base_path == "":
        cmd = "git diff " + file_name
    else:
        cmd = "cd " + base_path + AND + "git diff " + file_name
    print(cmd)
    result = my_os.process(cmd)
    print(result)
    if len(result) > 0:
        return True
    return False


def add_file(file_name, base_path=""):
    if base_path == "":
        cmd = "git add " + file_name
    else:
        cmd = "cd " + base_path + AND + "git add " + file_name
    print(cmd)
    result = my_os.process(cmd)
    print(result)
    if len(result) > 0:
        return False
    return True


def git_commit(commit_msg, base_path=""):
    if base_path == "":
        cmd = "git commit -m \"" + commit_msg + "\""
    else:
        cmd = "cd " + base_path + AND + "git commit -m \"" + commit_msg + "\""
    print(cmd)
    result = my_os.process(cmd)
    print(result)


def git_push(base_path=""):
    if base_path == "":
        cmd = "git push origin master"
    else:
        cmd = "cd " + base_path + AND + "git push origin master"

    print(cmd)
    result = my_os.process(cmd)
    print(result)


def git_clone(git_url, clone_path):
    cmd = "git clone " + str(git_url) + " " + clone_path
    print(cmd)
    result = my_os.process(cmd)
    print(result)


def git_pull(base_path=""):
    if base_path == "":
        cmd = "git pull"
    else:
        cmd = "cd " + base_path + AND + "git pull"

    print(cmd)
    result = my_os.process(cmd)
    print(result)


def last_commit_msg(base_path=""):
    if base_path == "":
        cmd = "git show --oneline"
    else:
        cmd = "cd " + base_path + AND + "git show --oneline"
    # cmd = "git show --oneline"
    print(cmd)
    result = my_os.process(cmd)
    if str(result[0]).__contains__("fatal:"):
        return None, None
    msg = result[0].decode("utf-8")
    commit_id = re.findall("(.*?)\s", msg)[0]
    commit_msg = str(msg)[len(commit_id):].strip()
    return commit_id, commit_msg


def check_file_have_add_git(file_name, base_path):
    if base_path == "":
        cmd = "git ls-files"
    else:
        cmd = "cd " + base_path + AND + "git ls-files"

    print(cmd)
    result = my_os.process(cmd)
    print(result)
    file_name = str(file_name).replace("\\", "/")
    for a in result:
        tmp = str(a.decode()).replace("\r", "").replace("\n", "")
        if file_name.endswith(tmp):
            return True
    return False


if __name__ == '__main__':
    print(check_file_have_add_git("git_utils.py", ""))
