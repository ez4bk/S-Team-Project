import sys
import traceback

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot

from config.client_info import config
from config.sql_query.client_query import add_to_inventory, exist_game_check
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher

sql_utils = SqlUtils()
aes_cipher = AESCipher()


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress

    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    # progress = pyqtSignal(int)


class Worker(QRunnable):

    def __init__(self, fn, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # self.kwargs = dict(kwargs)
        # self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            result = self.fn(**self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

    def handle_add_to_inventory_query(self):
        game_id = self.kwargs['game_id']
        parent_id = config['parent_id']
        try:
            res = sql_utils.sql_exec(exist_game_check.format(parent_id, game_id), 1)[0][0]
        except Exception as e:
            self.error.emit('Fetch database failed!')
            return
        if res == 1:
            self.error.emit("Game already in the inventory!")
            return
        else:
            try:
                sql_utils.sql_exec(add_to_inventory.format(parent_id, game_id), 0)
                self.finished.emit()
            except Exception as e:
                self.error.emit('Fetch database failed!')
                return
