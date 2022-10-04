import json
import os

import simplejson

from commonlib.base_lib.system_utils import fileutils, systemutils
from commonlib.base_lib.utils.processpath import cur_file_dir

frame_runner_backup_file = os.path.join(cur_file_dir(), "tmp", "tmp.json")
retry_flag = False


def load_config_file(file_name):
    if not os.path.exists(file_name):
        config = {}
    else:
        json_file = open(file_name, 'r', encoding="utf-8")
        config = simplejson.load(json_file)
        json_file.close()
    return config


def save_runner_result(json_buf):
    file_name = frame_runner_backup_file
    if not os.path.exists(file_name):
        fileutils.create_file(file_name)
        config = {}
    else:
        config = load_config_file(file_name)
    json_file = open(file_name, 'w+', encoding="utf-8")
    config["step_list"] = json_buf
    json_file.write(json.dumps(config))
    json_file.close()


def clear_runner_result():
    file_name = frame_runner_backup_file
    if not os.path.exists(file_name):
        return
    save_runner_result({})


def clear_runner_id_result(runner_id):
    config = load_runner_result()
    if runner_id in config:
        config[runner_id] = {"flag": ""}
    save_runner_result(config)


def load_runner_result():
    file_name = frame_runner_backup_file
    if not os.path.exists(file_name):
        config = {}
    else:
        json_file = open(file_name, 'r', encoding="utf-8")
        config = simplejson.load(json_file)
        json_file.close()
        if "step_list" in config:
            config = config["step_list"]
    return config


def set_retry_flag(retry):
    global retry_flag
    retry_flag = retry


def get_retry_flag():
    global retry_flag
    return retry_flag
