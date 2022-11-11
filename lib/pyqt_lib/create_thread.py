from PyQt6.QtCore import QThread


def create_thread(worker, query):
    thread = QThread()
    worker.moveToThread(thread)
    thread.started.connect(query)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    return thread
