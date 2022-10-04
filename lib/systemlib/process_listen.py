import psutil


class ProcessListen(object):
    def __init__(self):
        pass

    @staticmethod
    def find_process_by_name(keyword):
        """
        Find the process by keyword fuzzy matching
        :param keyword: keyword of the process
        :return proc_list: list of matching process id
        """
        proc_list = []
        for p in psutil.process_iter(['name', 'pid', 'status']):
            try:
                if keyword in p.info['name'] and p.info['status'] == 'running':
                    p_dict = {
                        'name': p.info['name'],
                        'pid': p.info['pid']
                    }
                    proc_list.append(p_dict)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return proc_list


if __name__ == '__main__':
    ProcessListen.find_process_by_name('')
