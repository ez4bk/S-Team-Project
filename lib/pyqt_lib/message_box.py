from PyQt6.QtWidgets import QMessageBox


def message_info_box(parent, msg_str):
    """
    Pull up a message box.

    :param parent: parent window the msg box belongs to
    :param msg_str: message text
    :return: Null
    """
    QMessageBox.information(parent, 'FamiOwl Information', msg_str)
