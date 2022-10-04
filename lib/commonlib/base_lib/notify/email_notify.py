# -*- coding: utf-8 -*-


from lib.commonlib.base_lib.notify.auto_email import Staff, SimpleEmail
from lib.commonlib.base_lib.notify.email_utils import Attachment


class MailNotify(object):
    """
    代码示例::

        notify_utils = NotifyUtils()
        mail_title = "Notify_Utils"
        mail_msg = "NotifyUtils调试Demo"
        mail_file = []
        mail_to_address = ["linhuan@ruijie.com.cn"]
        support_address = [("debug1", "debug1@ruijie.com.cn"), ("demo1", "demo1.ruijie.com.cn")]

        notify_utils.set_mail_config(mail_title, mail_msg, mail_to_address, mail_file, support_address)
        notify_utils.send_mail()
    """

    def __init__(self):
        self.__support_address = []  # 支持人员邮件地址列表
        self.__mail_title = ""  # 邮件标题
        self.__mail_msg = ""  # 邮件内容
        self.__mail_to_address = []  # 邮件发送到
        self.__mail_file = []  # 邮件必发送的附件
        self.__attachment_root = ""
        pass

    def set_mail_config(self, mail_title, mail_msg, mail_to_address, mail_files, support_address=None):
        """
        配制邮件信息。进行邮件发送前，需要调用此接口，配制邮件信息

        :param mail_title: 邮件标题，类型为str
        :param mail_msg: 邮件内容，类型为str
        :param mail_to_address: 邮件发送的接收者列表，需要填写完整的邮件地址,类型为list。如：["test@ruijie.com.cn"]
        :param mail_files: 附件列表，类型为list
        :param support_address: 支持者地址列表
        """
        self.__mail_title = mail_title
        self.__mail_msg = mail_msg
        self.__mail_file = mail_files
        self.__mail_to_address = mail_to_address
        self.__support_address = support_address
        self.__attachment_root = "http://192.168.1.1/result/attachement"

    def __init_config(self):
        """
        初始化配制，用来处理set_mail_config的数据内容
        """
        tmp = []
        for support_item in self.__support_address:  # 将支持都邮件地址，转换成Staff类型
            tmp.append(Staff(name=str(support_item[0]), addr=str(support_item[1])))
        self.__support_address = tmp
        tmp = []
        for mail_file in self.__mail_file:  # 将邮件地址转换成Attachment类型
            tmp.append(Attachment(path=str(mail_file)))
        self.__mail_file = tmp

    def send_mail(self):
        """
        发送邮件，此函数为异步操作，提示成功后，并不表示用户已经收到邮件

        """
        self.__init_config()
        SimpleEmail(attachment_root=self.__attachment_root,
                    support_staffs=self.__support_address
                    ).send(to_addrs=self.__mail_to_address,
                           subject=self.__mail_title,
                           message=self.__mail_msg,
                           attachments=self.__mail_file)


if __name__ == '__main__':
    notify_utils = MailNotify()
    tmp_mail_title = "Notify_Utils"
    tmp_mail_msg = "NotifyUtils调试Demo"
    tmp_mail_file = []
    tmp_mail_to_address = ["huan_lin@ruijie.com.cn"]
    tmp_support_address = [("debug1", "debug1@ruijie.com.cn"), ("demo1", "demo1@ruijie.com.cn")]

    notify_utils.set_mail_config(tmp_mail_title, tmp_mail_msg, tmp_mail_to_address, tmp_mail_file, tmp_support_address)
    notify_utils.send_mail()
