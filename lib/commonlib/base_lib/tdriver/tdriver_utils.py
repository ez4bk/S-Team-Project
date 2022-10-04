# coding=utf-8
from lib.commonlib.base_lib.tdriver.process_interface import ProcessInterface


def check_depend(depend_list, process_result_list):
    for a in depend_list:
        if a in dict(process_result_list).keys():
            if not process_result_list[a]:
                return False
        else:
            return False


def get_all_process_interface_list(obj):
    """

    :param obj:
    :return:
    """
    tmp_list = []
    # print(dir(obj))
    for a in dir(obj):
        if a == "__class__":
            continue
        tmp = getattr(obj, a)
        # print(tmp)
        if isinstance(tmp, ProcessInterface.__class__):
            tmp_list.append(tmp)
            tmp_list += get_all_process_interface_list(tmp)
    return tmp_list


class DemoObj(object):
    class AProcess(ProcessInterface):
        class CProcess(ProcessInterface):
            def run(self):
                print("Cprocess")

        def run(self, **kwargs):
            print("Aprocess")

    class BProcess(ProcessInterface):
        def run(self, **kwargs):
            print("Bprocess")


if __name__ == '__main__':
    dd = get_all_process_interface_list(DemoObj())
    print(dd)
